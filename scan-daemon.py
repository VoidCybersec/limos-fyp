import time
import datetime
import requests
import urllib.parse
from checksumdir import dirhash

#Function to send an alert message directly to someone on Telegram using the @LwfimAlertBot
def telegramalert(altname, dirname, currenttime, currentdate):
    #TOKEN is the API token of the bot, CHAT_ID is the chat_id of Telegram of the receipient
    TOKEN = ""
    CHAT_ID = ""
    #message to be sent
    alerttext = f"ALERT!\nThe intergrity of the folder {altname}({dirname}) has been breached!\nScanned at {currenttime} on {currentdate}."
    #URL encoding of the messsage so that browsers are able to read it
    urlencoded_alerttext = urllib.parse.quote(alerttext)
    #web get reqeust to send the message throught the bot
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={urlencoded_alerttext}")

#function to scan folder and check if the baseline hash matches up with the newly scannned hash
def runscan(altname, dirname, currenttime, currentdate, currenthash, scanhist):
    #if the new hash is not the same as the baseline, status is updated to irregular and a alert is sent with Telegram
    if (currenthash != basehash):
        status = "irregular"
        telegramalert(altname, dirname, currenttime, currentdate)
    elif (currenthash == basehash):
        status = "identical"
    else:
        print("Error")
    
    #writes the latest scan details to the scan log file
    scanhist.write(f"{currenttime}:{currentdate}:{currenthash}:{status}\n")

#opens allscans.txt and parses each line to each section
with open("/home/void/Documents/fyp-fim-thigendra/allscans.txt", "r") as f:
    #read each line in allscans.txt
    for line in f:
        values_allscans = line.strip().split(":")
        timenow = time.time()
        altname = values_allscans[0]
        dirname = values_allscans[1]
        scantime = values_allscans[2]
        basehash = values_allscans[3]

        #opens scan log file of specified scan file
        with open(f"/home/void/Documents/fyp-fim-thigendra/scan-history/{altname}-log.txt", "a+") as scanhist:
            #sets pointer to start of file
            scanhist.seek(0)
            #reads each line of scan log file and parses the 
            for line in scanhist:
                values_scanhist = line.strip().split(":")
                timehist_str = values_scanhist[0]
                datehist_str = values_scanhist[1]
                #formatting for time formates in the scan log
                timehist = datetime.datetime.strptime(timehist_str, "%H-%M-%S")
                datehist = datetime.datetime.strptime(datehist_str, "%Y-%m-%d")
                datetimehist = datetime.datetime.combine(datehist, timehist.time())
                #gets the current time and stores in a variable
                currentdatetime = datetime.datetime.now()
                #calculates the difference in time from current time and the last scan time
                diff = currentdatetime - datetimehist
                #formats back the current time and date for storage in the scan log file
                currenttime = time.strftime("%H-%1M-%S")
                currentdate = time.strftime("%Y-%m-%d")
                #makes a hash in MD5 
                currenthash = dirhash (dirname, 'md5')

                #checks the frequency of the scan, for each frequency (daily, weekly, monthly) it checks if it has been more than a day, week, or month respectively. If it has, runscan function runs
                if (scantime == "daily"):
                    if (diff.days >= 1):
                        runscan(altname, dirname, currenttime, currentdate, currenthash, scanhist)
                elif (scantime == "weekly"):
                    if (diff.days >= 7):
                        runscan(altname, dirname, currenttime, currentdate, currenthash, scanhist)
                elif (scantime == "monthly"):
                    if (diff.days >= 30):
                        runscan(altname, dirname, currenttime, currentdate, currenthash, scanhist)
                else:
                    print("file is empty")
    