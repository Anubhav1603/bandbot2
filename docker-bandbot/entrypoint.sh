#!/bin/sh

read -p "Press enter to continue" REPLY
read -p "Press enter to continue" REPLY

if [ -f /bandbot2/teletoken.py ]; then
    python3.8 start.py
else
    echo "Missing teletoken.py file"
    if [ "$FILETOKEN" = "DEFAULT" ]; then
        echo "Missing environment variable FILETOKEN"
    else
        wget -O /bandbot2/teletoken.py $FILETOKEN
        if [ $? -ne 0 ]; then
            echo "Unknown error occured while downloading teletoken file from $FILETOKEN. Please restart container with correct URL."
        else
            echo "teletoken downloaded successfully. Please restart container."
        fi
    fi
fi