#!/bin/bash
# ONLY RUN THIS SCRIPT FROM ITS ORIGINAL DIRECTORY

sudo pip3 install -r requirements.txt
crontab -l | { cat; echo "0 * * * * /usr/bin/python3 $(pwd)/scan-daemon.py"; } | crontab -
