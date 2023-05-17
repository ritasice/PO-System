import pandas as pd
import csv
import pyodbc
from Routes.model import User
from Routes import db

# Set up the connection details
server = '10.0.1.218'
database = 'ritas_po_system'
username = 'INTAPPS'
password = 'ritasit#@#$qwer'
driver = '{ODBC Driver 18 for SQL Server}'

# CSV file path
csv_file = '/home/dpatel/PO-System/users.csv'

# Establish the database connection
driver = "{ODBC Driver 18 for SQL Server}"  # replace with the appropriate driver for your system
conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};trusted_connection=yes;Encrypt=no"

conn = pyodbc.connect(conn_str)   
cursor = conn.cursor() 

with open(csv_file, 'r') as file:
    csv_reader = csv.reader(file)

# Iterate over each row and insert it into the SQL Server database
    for line in csv_reader:
        '''
        ['displayname', 'city', 'company', 'department', 'EmailAddress', 'telephonenumber']
        '''
        
        
        
        if line[4].endswith('@ritascorp.com'):
            if line[3] == '':
                continue
            Name = line[0]
            email = line[4]
            department = line[3]
            if department == 'ops':
                department = 'Operations'
            elif department == 'R & D':
                department = 'R&D'
            elif department =='Procurement':
                department = 'Supply Chain'
            elif department == 'Franchise Sales':
                department = 'Sales'
            elif department == 'Facilities':
                department = 'HR'
                
            query = f"INSERT INTO [dbo].[users] (Name, Email, Department) VALUES ({Name}, {email}, {department});"
            cursor.execute(query)
            cursor.commit()
            
conn.close()
            
        
            
            
            
                
            
    

# Close the database connection
# conn.close()
