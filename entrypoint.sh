#!/bin/sh

if [ -f /bandbot2/teletoken.py ]; then
    python3.8 /bandbot2/start.py
else
    if [ "$FILETOKEN" = "DEFAULT" ]; then
        echo "Missing environment variable FILETOKEN"
    else
        wget -O /bandbot2/teletoken.py $FILETOKEN
        if [ $? -ne 0]; then
            echo "Unknown error occured while downloading teletoken file"
        else
            echo "teletoken downloaded successfully. Please restart container."
    fi
fi