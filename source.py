#!/usr/bin/env python
import os
import sys
import sqlite3

database_name = "Transaction_details.db"
table_name = "Transactions"

# List of documents that need to be parsed
# document_list=["U16571275.pdf","U16572745.pdf","U16573131.pdf"]

# bash script to convert pdf to txt 
command="pdf2txt.py -o "

document_list=[]
for i in range(1,len(sys.argv)):
    document_list.append(sys.argv[i])
print(document_list)
print(len(document_list))

# Establishing a connections to sqlite server database
try:
    connection = sqlite3.connect(database_name)
    # Getting cursor of the connections
    cur = connection.cursor()
except:
    print("Oops!",sys.exc_info()[0],"occured.")
    


# Executing a SQL query to create table 
# which will store the important details from the parsed pdf file
cur.execute("CREATE TABLE IF NOT EXISTS "+ table_name +\
                                  "(SRN VARCHAR(10) PRIMARY KEY,\
                                   Date_of_transaction DATE,\
                                   Bank TEXT,\
                                   Name VARCHAR(100),\
                                   Address TEXT,\
                                   Type_of_Service VARCHAR(500),\
                                   Service_Description TEXT,\
                                   Type_of_fee VARCHAR(100),\
                                   Amount FLOAT,\
                                   Total FLOAT,\
                                   Payment_received TEXT,\
                                   Mode_of_payment TEXT\
                                   );")
# for loop to parse single document at a time and storing the data to sql database 
for document in document_list:
    # making a temporary text file to save contents of pdf in .txt format
    txtfile=document[:-4]+".txt"
    
    # running bash script to convert pdf to text
    os.system(command+txtfile+" "+document)
    try:
        # opening the generated .txt file to read its contents
        file = open(txtfile,"r");   
        
        # reading all the lines of txt file
        lines=file.readlines()
        for line in lines:  # for loop to delete empty lines 
            if line =='\n': #from the list of read lines
                lines.remove(line)
            
       
        file.close()  #closing the temporary text file
        os.remove(txtfile)  # deleting the temporary text file
    except:
        print("Oops!",sys.exc_info()[0],"occured.")
    numOfLines=len(lines) # counting the number of lines
    
    # Now parsing the read lines 
    # and scraping the useful data from a list of strings
    
    temp_date=lines[3][-11:].strip().split("/")    
    temp_date.reverse()          # converting read date to format supported by SQL
    date="-".join(temp_date)     # ie. YYYY-MM-DD

    SRN=lines[4][-10:].strip()
    bank=lines[6].strip()
    name=lines[10].strip()
    address=''.join(lines[11:15])
    serviceType=lines[16][14:].strip()   
    serviceDescription=''.join(lines[20:23])
    typeOfFee=lines[23].strip()
    try:
        amount=float(lines[24].strip()) # converting string to float, as currency
        total=float(lines[26].strip())
    except ValueError:
        print("Value error occured , string value cannot be converted to float\n")
        amount=total=0
        
    receivedPayment=lines[28][26:].strip()      
    modeOfPayment=lines[29].strip()
    
    # SQL query to check if the current pdf file data 
    # already exists in the table as SRN is set as PRIMARY KEY 
    cur.execute("SELECT COUNT(*) FROM Transactions WHERE SRN='"+SRN+"';")
    result=cur.fetchone()[0]
    if result == 0 :
        insertQuery="INSERT INTO Transactions VALUES('" + SRN +"','"\
                                                 + date +"','"\
                                                 + bank +"','"\
                                                 + name +"','"\
                                                 + address +"','"\
                                                 + serviceType +"','"\
                                                 + serviceDescription +"','"\
                                                 + typeOfFee +"',"\
                                                 + str(amount)+","\
                                                 + str(total) +",'"\
                                                 + receivedPayment +"','"\
                                                 + modeOfPayment+"');"
  
        cur.execute(insertQuery) # running SQL query to enter values in table
connection.commit()  # saving the data to SQL database
connection.close()   # closing the connection to sql server