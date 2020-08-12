import requests
import os

class NoManifestError(Exception): pass
class InvalidDirectoryError(Exception): pass
class NoRemoteFileError(Exception): pass

class WebStorage():
    def __init__(self, endpoint, directory):
        if endpoint[-1] == "/":
            self.endpoint = endpoint
        else:
            self.endpoint = endpoint + "/"
        
        if directory[-1] == "/":
            self.directory = directory
        else:
            self.directory = directory + "/"
        
        if not os.path.isdir(self.directory):
            raise InvalidDirectoryError
        
    def _getFile(self, fpath):
        f = open(self.directory + fpath, mode = "wb")
        res = requests.get(self.endpoint + self.dbname + "/" + fpath)
        
        if res.status_code != 200:
            f.close()
            raise NoRemoteFileError
        else:
            f.write(res.content)
            f.close()

    def sync(self):
        res = requests.get(self.endpoint + "manifest.json")

        if res.status_code != 200:
            raise NoManifestError
        
        print("fsync: syncing DB " + res.json()["name"])
        self.dbname = res.json()["name"]
        res = res.json()["data"]

        for elem in res:
            # Mutable File
            if elem[1]:
                self._getFile(elem[0])
            # Immutable File
            else:
                if not os.path.isfile(self.directory + elem[0]):
                    self._getFile(elem[0])