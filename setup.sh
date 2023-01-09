#! /bin/bash

#install necessary packages to sudo enviroment
sudo pip3 install -r requirements.txt
#make script executable
chmod +x scan-daemon.py
#add script to crontab
crontab -l > temp/crontab-temp
echo "0 * * * * /usr/bin/python3 /home/void/Documents/fyp-fim-thigendra/scan-daemon.py" >> temp/crontab-temp
crontab temp/crontab-temp
rm temp/crontab-temp