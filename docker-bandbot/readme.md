# docker-bandbot2

Standalone bandbot client with headless chrome

## Dockerfile

[`kohs100/bandbot2` Dockerfile](Dockerfile)

## Teletoken file

[Sample teletoken file](sample_teletoken.py)

Please create your teletoken.py file and make sure it is accessible through the URL_TO_teletoken.py

## How to use this image
* Initialize
```
$ docker run --name CONTAINER_NAME -i -t -e FILETOKEN=URL_TO_teletoken.py kohs100/bandbot2
# Press Enter to continue
```
* Run
```
# docker start -e FILETOKEN=URL_TO_teletoken.py CONTAINER_NAME
$ docker start CONTAINER_NAME

$ docker attach CONTAINER_NAME
# Press ^P^Q to detach container stdin
```