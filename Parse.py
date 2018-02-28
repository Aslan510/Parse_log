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

def main():
# generates a dictionary to fit the 12 months 
    data = {x:{} for x in range(1,13)}  


 # check if file exists
    if not os.path.exists(fileName):  

        print("No cached " + fileName + " found.\nDownloading from: " + url)
# Saves file as http.log
        getDataFile() 

    else:

        print("Using already downloaded file " + fileName + " file.")

# parses data file, and sorts by month        

    parseLogs(data) 

    print("Events Per Day for each month:")

    successCode = 0

    ClientErrorCode = 0

    ServerErrorCode = 0
    
    RedirectCode = 0
    
    TotalCodesPulled = 0

    for monthNum, month in data.items(): # for each dictionary in data

        print(monthName[monthNum] + ":" ) # prints name of month

        for dayNum, logs in month.items(): # iterate through each day of logs

            print("\t" + str(dayNum) + ": " + str(len(logs)) + " events.")

            for log in logs: # iterate through each log dictionary contained in the logs list

                logCode=log['code']

                if 199<logCode<300:

                    successCode+=1
                if 299<logCode<400:
                    
                    RedirectCode+=1

                if 399<logCode<500:

                    ClientErrorCode+=1

                if 499<logCode<600:

                    ServerErrorCode+=1
                    
    total = (successCode + RedirectCode + ClientErrorCode + ServerErrorCode)

    print("Successful requests: " + str(successCode))
    
    win = "{0:.0f}%".format((successCode/total * 100))
    
    print(win)

    print("Unsuccessful requests: " + str(ClientErrorCode + ServerErrorCode))
    
    bad = (ClientErrorCode + ServerErrorCode)
    
    loss = "{0:.0f}%".format((bad/total * 100))
    
    print(loss)

    print("Redirected Requests: " + str(RedirectCode))
    
    re = "{0:.0f}%".format((RedirectCode/total * 100))
    
    print (re)
    
    print ("Toal numbr of reguest: ", total)
    
if __name__ == "__main__":

    main()
