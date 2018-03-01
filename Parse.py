from urllib.request import urlopen
import os
import re
import datetime
import time



def parseLogs(data):
#opens log file
    with open(fileName, 'r') as logFile: 

        print("Parsing Data ...")

#Key and values set up for the matrix
        monthNum = {v: k for k, v in monthName.items()}  

        current_line = 0
# list of all failed parses
        FailedLog = [] 
# goes through file

        for line in logFile: 
            current_line += 1 

            splitData = re.split('.*\[(.*?):.*\] \".* (.*) .*\" (\d{3})', line)

            if len(splitData) == 5: 

                dateSplit = splitData[1].split('/') # splits up day/month/year string

                date = datetime.date(int(dateSplit[2]), monthNum[dateSplit[1]], int(dateSplit[0])) 

                logData = {'date': date, 'name':splitData[2], 'code':int(splitData[3])} 

                if date.day in data[date.month]: 

                    data[date.month][date.day].append(logData) # append dictionary containing log data

                    
                else:

                    data[date.month][date.day] = [logData] 
            else: 

                FailedLog.append(splitData) 
                
        print(str(len(FailedLog)) + " lines couldn't be parsed.")
        
# Downloads http log to "http.log"
def getDataFile(): 
# creates a lof file if there is not one already
    with open(fileName, 'wb') as logFile: 
# connect to server
        with urlopen(url) as stream: 
            
            fileSize = stream.length

            print("Downloading \"%s\" (%s KB)...\n" % (fileName, fileSize / 1000))

            currentFileSize = 0

            blockSize = 8192

            while True: 

                buffer = stream.read(blockSize)

                if not buffer: 

                    break

                currentFileSize += len(buffer) 

                logFile.write(buffer)

                status = r"%10d [%3.2f%%]" % (currentFileSize, currentFileSize*100. / fileSize) 

                status = status + chr(8)*(len(status) + 1)

                print(status, end="") 
            
            print("", end="\n") 
#url address to pull the log file        
url = "https://s3.amazonaws.com/tcmg476/http_access_log"
#naming the file        
fileName = "http.log"
#setting up the dates        
monthName = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'} # Maps month num (key) to name (value)

def countEvents(month):
    sum = 0
    for dayNum, logs in month.items():
        sum += len(logs)
    return sum
def main():
# generates a dictionary to fit the 12 months 
    data = {x:{} for x in range(1,13)}  


 # check if file exists
    if not os.path.exists(fileName):  

        print("Your file was not previously downloaded. " + fileName + " found.\nDownloading your file from: " + url)

        getDataFile() 

    else:

        print("Congrats you already have the file downloaded. " + fileName + " Let's get started.")

# parses data file, and sorts by month        

    parseLogs(data) 
    
    #print("Lines per month")

    #print("Lines Per Day for each month:")

    successCode = 0

    ClientErrorCode = 0

    ServerErrorCode = 0
    
    RedirectCode = 0
    
    TotalCodesPulled = 0
 #blank file name log   
    fileNames = {}

    for monthNum, month in data.items(): 
#prints the totals for the given month 
        print(monthName[monthNum] + ": " +str(countEvents(month)) + " Lines for this month")
#prints the totals for each day of the month
        for dayNum, logs in month.items():

            print("\t" + str(dayNum) + ": " + str(len(logs)) + " Lines.")

            for log in logs: 

                HTTPCode=log['code']

                if 199<HTTPCode<300:

                    successCode+=1
                    
                if 299<HTTPCode<400:
                    
                    RedirectCode+=1

                if 399<HTTPCode<500:

                    ClientErrorCode+=1

                if 499<HTTPCode<600:

                    ServerErrorCode+=1
                    
                                    
 #count the different types of filenames being accessed                   
                if log["name"] in fileNames:
                    fileNames[log["name"]] += 1
                else:
                    fileNames[log["name"]] = 1   
 #sort the log for the file names                   
    sorted_fileNames = sorted(fileNames.items(), key=lambda x: x[1])
    
    print("\nThe most requested file was: " + sorted_fileNames[-1][0] + " (accessed " + str(sorted_fileNames[-1][1]) + " times)")
                    
    print("The least requested file was: " + sorted_fileNames[0][0] + " (accessed " + str(sorted_fileNames[0][1]) + " time / times)")    
                    
    total = (successCode + RedirectCode + ClientErrorCode + ServerErrorCode)

    print("Successful requests: " + str(successCode))
    
    win = "{0:.0f}%".format((successCode/total * 100))
    
    print(win)

    print("Unsuccessful requests: " + str(ClientErrorCode + ServerErrorCode))
    
    Failed = (ClientErrorCode + ServerErrorCode)
    
    loss = "{0:.0f}%".format((Failed/total * 100))
    
    print(loss)

    print("Redirected Requests: " + str(RedirectCode))
    
    re = "{0:.0f}%".format((RedirectCode/total * 100))
    
    print (re)
    
    print ("Toal numbr of reguest: ", total)
       
      
    print("Thank for trying this out and have a great Day!")
    
    
if __name__ == "__main__":

    print("We will go through the log file and find the information we needed.")
    time.sleep(2)
    print("The first part will say how many lines of the file could not be parsed.")
    time.sleep(2)
    print("The second part will show the total line count for the month.")
    time.sleep(2)
    print("The month is then broken down into each day with their total line count.")
    time.sleep(2)
    print("Next it will show the most and least used file names.")
    time.sleep(2)
    print("Then it will follow up with the rate of each type of action.")
    time.sleep(2)
    main()
