#!/bin/bash

sudo pip3 install -r requirements.txt
crontab -l | { cat; echo "0 * * * * /usr/bin/python3 /home/void/Documents/fyp-fim-thigendra/scan-daemon.py"; } | crontab -