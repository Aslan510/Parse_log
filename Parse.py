from urllib.request import urlopen
import os
import re
import datetime
import time



def Parse_Logs(data):
#opens log file
    with open(File_Name, 'r') as Log_File: 

        print("Extracting Data ...")

#Key and values set up for the matrix
        Month_Number = {v: k for k, v in Month_Name.items()}  

        current_line = 0
# list of all failed parses
        Failed_Log = [] 
# goes through file

        for line in Log_File: 
            current_line += 1 

            Split_Data = re.split('.*\[(.*?):.*\] \".* (.*) .*\" (\d{3})', line)

            if len(Split_Data) == 5: 

                Date_Split = Split_Data[1].split('/') # splits up day/month/year string

                date = datetime.date(int(Date_Split[2]), Month_Number[Date_Split[1]], int(Date_Split[0])) 

                Log_Data = {'date': date, 'name':Split_Data[2], 'code':int(Split_Data[3])} 

                if date.day in data[date.month]: 

                    data[date.month][date.day].append(Log_Data)

                    
                else:

                    data[date.month][date.day] = [Log_Data] 
            else: 

                Failed_Log.append(Split_Data) 
                
        print(str(len(Failed_Log)) + " lines couldn't be parsed.")
        
# Downloads http log to "http.log"
def Get_Data_File(): 
# creates a lof file if there is not one already
    with open(File_Name, 'wb') as Log_File: 
# connect to server
        with urlopen(url) as stream: 
            
            File_Size = stream.length

            print("Downloading \"%s\" (%s KB)...\n" % (File_Name, File_Size / 1000))

            Current_File_Size = 0

            Block_Size = 8192

            while True: 

                buffer = stream.read(Block_Size)

                if not buffer: 

                    break

                Current_File_Size += len(buffer) 

                Log_File.write(buffer)

                status = r"%10d [%3.2f%%]" % (Current_File_Size, Current_File_Size*100. / File_Size) 

                status = status + chr(8)*(len(status) + 1)

                print(status, end="") 
            
            print("", end="\n") 
#url address to pull the log file        
url = "https://s3.amazonaws.com/tcmg476/http_access_log"
#naming the file        
File_Name = "http.log"
#setting up the dates        
Month_Name = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'} # Maps month num (key) to name (value)

def Count_Events(month):
    sum = 0
    for Day_Num, logs in month.items():
        sum += len(logs)
    return sum
def main():
# generates a dictionary to fit the 12 months 
    data = {x:{} for x in range(1,13)}  


 # check if file exists
    if not os.path.exists(File_Name):  

        print("Your file was not previously downloaded. " + File_Name + " found.\nDownloading your file from: " + url)

        Get_Data_File() 

    else:

        print("Congrats you already have the file downloaded. " + File_Name + " Let's get started.")

# parses data file, and sorts by month        

    Parse_Logs(data) 
    
    #print("Lines per month")

    #print("Lines Per Day for each month:")

    Success_Code = 0

    Client_Error_Code = 0

    Server_Error_Code = 0
    
    Redirect_Code = 0
    
    Total_Codes_Pulled = 0
 #blank file name log   
    File_Names = {}

    for Month_Num, month in data.items(): 
#prints the totals for the given month 
        print(Month_Name[Month_Num] + ": " +str(Count_Events(month)) + " Lines for this month")
#prints the totals for each day of the month
        for Day_Num, logs in month.items():

            print("\t" + str(Day_Num) + ": " + str(len(logs)) + " Lines.")

            for log in logs: 

                HTTP_Code=log['code']

                if 199<HTTP_Code<300:

                    Success_Code+=1
                    
                if 299<HTTP_Code<400:
                    
                    Redirect_Code+=1

                if 399<HTTP_Code<500:

                    Client_Error_Code+=1

                if 499<HTTP_Code<600:

                    Server_Error_Code+=1
                    
                                    
 #count the different types of filenames being accessed                   
                if log["name"] in File_Names:
                    File_Names[log["name"]] += 1
                else:
                    File_Names[log["name"]] = 1   
 #sort the log for the file names                   
    Sorted_fileNames = sorted(File_Names.items(), key=lambda x: x[1])
    
    print("\nThe most requested file was: " + Sorted_fileNames[-1][0] + " (accessed " + str(Sorted_fileNames[-1][1]) + " times)")
                    
    print("The least requested file was: " + Sorted_fileNames[0][0] + " (accessed " + str(Sorted_fileNames[0][1]) + " time / times)")    
                    
    total = (Success_Code + Redirect_Code + Client_Error_Code + Server_Error_Code)

    print("Successful requests: " + str(Success_Code))
    
    win = "{0:.0f}%".format((Success_Code/total * 100))
    
    print(win)

    print("Unsuccessful requests: " + str(Client_Error_Code + Server_Error_Code))
    
    Failed = (Client_Error_Code + Server_Error_Code)
    
    loss = "{0:.0f}%".format((Failed/total * 100))
    
    print(loss)

    print("Redirected Requests: " + str(Redirect_Code))
    
    re = "{0:.0f}%".format((Redirect_Code/total * 100))
    
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
