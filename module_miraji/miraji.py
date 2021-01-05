import csv
import glob
import API.fsync as fsync

from extensions import ModuleBase

DBENDPOINT = "https://bot.ster.email/miraji"
DBDIR = "module_miraji/images"

class get_DBError(Exception): pass
class update_DBError(Exception): pass
class check_dbError(Exception): pass

def chat(msg): return [("chat", msg)]
def image(path): return [("image", path)]

class Module(ModuleBase):
    commands = ["미라", "미라지", "미라티콘"]

    def __init__(self):
        self.cache = []
        try:
            self.update_DB()
        except FileNotFoundError:
            self.get_DB()
            self.update_DB()
            self.check_db()

    def run(self, params, usr_i):
        paramNum = len(params)

        try:
            self.update_DB()
        except FileNotFoundError:
            try:
                self.get_DB()
                self.update_DB()
                self.check_db()
            except get_DBError:
                return chat("miraji.py: DB 동기화 실패")
            except update_DBError:
                return chat("miraji.py: CSV 무결성검사 실패")
            except check_dbError:
                return chat("miraji.py: 이미지 무결성검사 실패")

        if paramNum == 3:
            name = params[2]

            if name == "갱신":
                try:
                    self.get_DB()
                    self.update_DB()
                    self.check_db()
                except get_DBError:
                    return chat("miraji.py: DB 동기화 실패")
                except update_DBError:
                    return chat("miraji.py: CSV 무결성검사 실패")
                except check_dbError:
                    return chat("miraji.py: 이미지 무결성검사 실패")
                else:
                    return chat("miraji.py: 미라지 갱신 성공")

            for elem in self.cache:
                if name == elem[0]: return image("module_miraji/"+elem[1])

            return chat("miraji.py: 미라지가 없습니다: " + name)
        else:
            return chat("miraji.py: 사용법\n!봇 미라 [미라지명]")


    def get_DB(self):
        try:
            stor = fsync.WebStorage(DBENDPOINT, DBDIR)
            stor.sync()
        except:
            raise get_DBError

    def update_DB(self):
        with open("module_miraji/images/miraji_dict.csv", "r", encoding = "utf-8") as f:
            rdr = csv.reader(f)
            self.cache = list(rdr)

        for elem in self.cache:
            if len(elem) != 2:
                raise update_DBError

    def check_db(self):
        file_list = glob.glob("module_miraji/images/*.*")
        
        for i, elem in enumerate(file_list):
            file_list[i] = elem.replace("\\", "/")
            file_list[i] = file_list[i][14:]

        for elem in self.cache:
            if not elem[1] in file_list:
                raise check_dbError
