import os
import time
import datetime
import subprocess
from fpdf import FPDF
from checksumdir import dirhash

#function using clear command of Linux to make program look clean in runtime
def bashclear():
    subprocess.run("clear")

#function to delete the scan from allscans.txt, log file, and report file based on the scan chosen to delete
def deletescan(altname):

    #reads allscans.txt
    with open("allscans.txt", "r") as f:
        all_scans = f.readlines()
        #goes through each line and parses the first value (scan name/altname)
        for i, scan in enumerate(all_scans):
            scan_data = scan.strip().split(":")
            #if the name is found, delete that whole line
            if scan_data[0] == altname:
                all_scans.pop(i)
                break

    #rewrites content of the file back to allscans.txt
    with open("allscans.txt", "w") as f:
        f.writelines(all_scans)

    #remove respective log file
    os.remove(f"scan-history/{altname}-log.txt")
    #remove respective report file
    
    #checks if the report file exists (stores boolean), if exist, remove it
    existence = os.path.exists(f"scan-report/{altname}-report.pdf")
    if (existence == True):
        os.remove(f"scan-report/{altname}-report.pdf")

    #prints the action done and goes back to mainpage
    print("Scan, log file, and report is deleted!")
    time.sleep(2)
    mainpage()

#function to make PDF report of the scan chosen (Report Generation)
def reportscan(altname, path, frequency, dhash):

    #save the current date and time
    current_datetime = datetime.datetime.now()

    #create PDF instance
    pdf = FPDF()
    #add a PDF page
    pdf.add_page()
    
    #add the APU logo to the corner of the page
    pdf.image("etc/apulogo.jpg", w = 25, h = 25)

    #set font and create title that include the scan name and date time of creation
    pdf.set_font("Arial", "B", size = 16)
    pdf.cell(200, 10, txt = f"Scan Report of {altname}", ln = 1, align = "C")
    pdf.cell(200, 10, txt = f"on {current_datetime}", ln = 1, align = "C")
    
    #set font and make a divider
    pdf.set_font("Arial", size = 12)
    pdf.cell(200, 10, txt = f"------------------------------------------------------------------------------------------------------------------------------", ln = 1, align = "C")

    #set font and print out title for first section
    pdf.set_font("Arial", "B", size = 12)
    pdf.cell(200, 10, txt = "Section 1: Scan Details", ln = 1, align = "L")
    
    #set font and print the details of the scan (scan name, directory of the scan, )
    pdf.set_font("Arial", size = 12)
    pdf.cell(200, 10, txt = f"Scan name -------------- : {altname}", ln = 1, align = "L")
    pdf.cell(200, 10, txt = f"Path ----------------------- : {path}", ln = 1, align = "L")
    pdf.cell(200, 10, txt = f"Frequency --------------- : {frequency}", ln = 1, align = "L")
    pdf.cell(200, 10, txt = f"Baseline Hash (MD5) - : {dhash}", ln = 1, align = "L")

    #set font and make a divider
    pdf.set_font("Arial", size = 12)
    pdf.cell(200, 10, txt = f"------------------------------------------------------------------------------------------------------------------------------", ln = 1, align = "C")

    #set font and print out title for second section
    pdf.set_font("Arial", "B", size = 12)
    pdf.cell(200, 10, txt = "Section 2: Permissions", ln = 1, align = "L")

    #set font and create a temp file in temp folder named ls-output.txt, this text file with contain the permission of all the files in the specified directory for scan
    pdf.set_font("Arial", size = 12)
    #opens ls-output.txt for reading
    with open("temp/ls-output.txt", "w") as f:
        #Linux commmand to list permmissions of file recursively
        subprocess.run(["ls", "-alR", path], stdout = f)
    #writes each line of ls-output.txt into the report
    with open("temp/ls-output.txt", "r") as f:
        for x in f:
            pdf.cell(200, 10, txt = x, ln = 1, align = "L")
    
    #set font and make a divider
    pdf.set_font("Arial", size = 12)
    pdf.cell(200, 10, txt = f"------------------------------------------------------------------------------------------------------------------------------", ln = 1, align = "C")

    #set font and print out title for third section
    pdf.set_font("Arial", "B", size = 12)
    pdf.cell(200, 10, txt = "Section 3: Scan History Log", ln = 1, align = "L")

    #set font
    pdf.set_font("Arial", size = 12)
    #opens respective log file and reads each line
    with open(f"scan-history/{altname}-log.txt", "r") as f:
        #writes each line of log file into the report
        for x in f:
            pdf.cell(200, 10, txt = x, ln = 1, align = "L")

    #set author for pdf
    pdf.set_author("Thigendra Colin Void Dupuis")

    #outputs the scan report with the scan name into scan-report directory
    pdf.output(f"scan-report/{altname}-report.pdf")

    #prints the action done and goes back to mainpage
    print(f"PDF Report saved to scan-report/{altname}-report.pdf !!")
    time.sleep(5)
    mainpage()
    
#function for viewing all the scans
def viewdir():
    bashclear()

    # Open the allscans.txt file
    with open("allscans.txt", "r") as f:
        # Read the lines in the file
        lines = f.readlines()

        # Print the list of scans and parses each line into its sections
        for i, line in enumerate(lines):
            values = line.strip().split(":")
            altname = values[0]
            path = values[1]
            
            #prints each line but only the scan name and scan directory sections in this format --> scan-name(scan-directory)
            print(f"{i+1}. {altname} ({path})")

        #user input to choose a scan
        selection = input("\nChoose a scan (eg. 1, 2, etc): ")
        
        #selects the scan
        selection = int(selection)
        selected_scan = lines[selection - 1]

        # Split the selected scan into its sections
        selected_values = selected_scan.strip().split(":")
        
        #sections of the scan
        altname = selected_values[0]
        path = selected_values[1]
        frequency = selected_values[2]
        dhash = selected_values[3]

        #views the scan chosen and its details, then prompts the user for action
        bashclear()
        print(f"You have selected the following scan:\n")
        print(f"Alternate name : {altname}")
        print(f"Path           : {path}")
        print(f"Scan frequency : {frequency}")
        print(f"Baseline hash  : {dhash}")

        #options for what to do
        print("\n1. Delete Scan\n2. Save PDF Report\n3. Mainpage \n")

        #while loop and case for chosen user action. if wrong choice, the loop stays true and prompts user again for a choice
        while True:
            #user input prompt
            option = input("Option: ")
            match option:
                case "1":
                    while True:
                        #asks user for confirmation of scan deletion
                        option = input("Confirm to delete? (y/n): ")
                        match option:
                            #if confirmed yes, deletescan func is invoked
                            case "y":
                                deletescan(altname)
                            case "n":
                                #if no, goes back to the mainpage
                                mainpage()
                            #invalid option prompts user again for a choice
                            case _:
                                print("Invalid Option! Please pick again!")
                #reportscan func is invoked and report of scan is generated
                case "2":
                    reportscan(altname, path, frequency, dhash)
                #goes back to main page
                case "3":
                    mainpage()
                #invalid option prompts user again for a choice
                case _:
                    print("Invalid Option! Please pick again!")

#function to check if scanname is unique
def checkaltname(name):
    #opens allscan.txt for reading
    with open("allscans.txt", "r") as f:
        #reads each line and parses the first section (scan name)
        for line in f:
            values = line.strip().split(":")
            #if the scan name exists, returns True
            if (values[0] == name):
                return True
    #if scan name doesn't exist, returns False
    return False

#function to save scan
def savescan(altname, dirname, scantime, dhash):
    #gets the current time and formats it in a human readable format
    currenttime = time.strftime("%H-%1M-%S")
    #gets the current date and formates it in a human readable formate
    currentdate = time.strftime("%Y-%m-%d")

    #opens allscans.txt for writing
    f = open("allscans.txt", "a+")
    #writes the scan details in a new line and makes a new line
    f.write(altname + ":" + dirname + ":" + scantime + ":" + dhash + "\n")
    #close the file for safe file handling purposes
    f.close()

    #creates a log file in scan-history directory
    f = open(f"scan-history/{altname}-log.txt", "a+")
    #writes the current time and and date, baseline hash and a short message saying that is the baseline hash into the log file
    f.write(currenttime + ":" + currentdate + ":" + dhash + ":" + "baseline-hash" + "\n")
    #close the file for safe file handling purposes
    f.close()

    #prints out success message and goes back to mainpage
    print("Directory has been successfully added for scanning!")
    time.sleep(2)
    mainpage()

#fucntion for initializing a directory for scan
def initdir():
    bashclear()
    print(" _______________________________________________________________")
    print("|                                                               |")
    print("| You are now about to initialize a directory for monitoring!   |")
    print("|_______________________________________________________________|")
    
    #prompts user for the full scan directory path
    dirname = input("Full directory path for scanning                 : ")
    #prompts user for the scan name that will be used 
    altname = input("Scan name of the specified directory             : ")

    #scan frequency selection in a while loop
    while True:
        #prompt user for how often the scan should take place
        scantime = input("Set scan frequency (daily/weekly/monthly)        : ")
        match scantime:
            case "daily":
                scantime = "daily"
                break
            case "weekly":
                scantime = "weekly"
                break
            case "monthly":
                scantime = "monthly"
                break
            case _:
                print("Invalid Option! Please pick again!")

    #asks the user if the entered details are correct or not
    print("\nAre these details correct?")
    print(f"Directory           : {dirname}")
    print(f"Alternate Name      : {altname}")
    print(f"Scan Frequency      : {scantime}")

    #checks all details in a while loop
    while True:
        #prompts user for confirmation
        option = input("\nConfirm? ('m' to go back to mainpage) (y/n/m) : ")
        match option:
            #if confirmed, neccessary checks are made
            case "y":
                #checks if the directory path exists (stores boolean)
                existence = os.path.exists(dirname)
                #checks if the scan name is unique and doesn't exist
                uniquename = checkaltname(altname)
                #if path exists and scan name is unique, savescan func is invoked and the scan is saved
                if (existence == True):
                    if (uniquename == False):
                        #hash is created and passed through savescan func
                        dhash = dirhash (dirname, "md5")
                        savescan(altname, dirname, scantime, dhash)
                    #prints error message if scan name isn't unique and goes back to mainpage
                    else:
                        print("Scan name already exists!")
                        time.sleep(5)
                        mainpage()
                #prints error message if directory doesn't exist and goes back to mainpage
                else:
                    print("The directory specified does not exist!")
                    time.sleep(5)
                    mainpage()
            #if no, user is back to initialize directory prompt
            case "n":
                initdir()
            #if m, goes back to mainpage (used in case no scan is meant to be initialized)
            case "m":
                mainpage()
            #prompts user again if other than y,n,m was selected
            case _:
                print("Invalid option!")

#function to print out the mainpage and it's choices
def mainpage():
    bashclear()
    print(" _______________________________________________________________")
    print("|                                                               |")
    print("| Welcome to the Lightweight File Intergrity Monitoring System! |")
    print("|        Created by Thigendra Colin Dupuis A.K.A Void           |")
    print("|_______________________________________________________________|")
    print(" \n1.Initialize Directory\n2.View Directories\n3.Exit\n")

    while True:
        option = input("Choice: ")
        match option:
            #if 1, initdir func is invoked
            case "1":
                initdir()
            #if 2, viewdir func is invoked
            case "2":
                viewdir()
            #if 3, exits the program
            case "3":
                exit()
            #if invalid option, prompts the user for choice again
            case _:
                print("Invalid option!")

#!!!!START OF PROGRAM!!!!
mainpage()