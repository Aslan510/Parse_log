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

        currline = 0
# list of all failed parses
        badLog = [] 
# iterate through file

        for line in logFile: 
            currline += 1 

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
