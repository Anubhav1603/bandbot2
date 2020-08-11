# Docker-bandbot

Selenium Standalone Server with Chrome

## Dockerfile

[`kohs100/bandbot2` Dockerfile](Dockerfile)

## How to use this image

```
# Initialize
$ docker run -i -t -d --name CONTAINER_NAME -e FILETOKEN=URL_TO_teletoken.py kohs100/bandbot2

# Run
$ docker start CONTAINER_NAME
```

