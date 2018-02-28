from urllib.request import urlopen
import os
import re
import datetime

# Sorts logs by month, and then by day in the "data" dictionary.  

def parseLogs(data):
#opens log file
    with open(fileName, 'r') as logFile: 

        print("Parsing Data ...")

#Key and values set up for the matrix
        monthNum = {v: k for k, v in monthName.items()}  

        current_line = 0
# list of all failed parses
        badLog = [] 
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

                badLog.append(splitData) 
                
        print(str(len(badLog)) + " lines couldn't be parsed.")
        
# Downloads http log to "http.log"
def getDataFile(): 
# creates a lof file if there is not one already
    with open(fileName, 'wb') as logFile: 
# connect to server
        with urlopen(url) as stream: 
            
            fileSize = stream.length

            print("Downloading \"%s\" (%s KB)..." % (fileName, fileSize / 1000))

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
