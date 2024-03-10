import requests
import json
import pandas as pd
from datetime import date
import time
import os

class Scheme():
    def __init__(self):
        self.response = requests.get("http://192.168.0.167:30000/drivers-licenses/list")
        self.json_format = json.loads(self.response.text)

    #Q1
    def is_suspended(self, file_name):
        suspended=[]
        for x in self.json_format:
            if x.get("suspendat") == True:
                suspended.append(x)
        self.save_file(suspended, file_name)

    #Q2
    def valid_licenses(self, file_name):
        today = date.today()
        valid_licenses = []
        for x in self.json_format:
            issue_str = x.get('dataDeEmitere')
            issue= self.convert_date(issue_str)            
            if issue <= today:
                valid_licenses.append(x)       
        self.save_file(valid_licenses, file_name)


    def convert_date(self, date_str):
        day, month, year = date_str.split("/")
        try:
            x= date(int(year), int(month), int(day))
            return x
        except ValueError:
            return None
    
    #Q3
    def find_by_category(self, file_name):
        cat_count = {}
        for x in self.json_format:
            cat = x["categorie"]
            if cat not in cat_count:
                cat_count[cat] = 0
            cat_count[cat] += 1
        self.save_file(cat_count, file_name)

    #function to save to excel files format
    def save_file(self, my_list, file_name):
        excel_filename = file_name + '.xlsx'

        if not isinstance(my_list, dict):
            df = pd.DataFrame(my_list)
            df.to_excel(excel_filename, index=False)
        else:
            df = pd.DataFrame.from_dict(my_list, orient='index', columns=['Count'])
            df.to_excel(excel_filename, index=True)
        
        print('Excel file created:', excel_filename)
    
        
def main():
    value=True
    accepted_values=[0,1,2,3]
    scheme = Scheme()

    while value is True:
        print("Options:\n1 to list suspended licenses\n2 to list licenses issued until today's date\n3 to find licenses based on category and their count\n0 to close the program\n")    
        command= int(input("Please select an input: "))
        if command not in accepted_values:
            print("Incorrect Input")
            time.sleep(1)
            if os.name == 'nt':
                os.system("cls")
            else:
                os.system('clear') 
            continue
        
        if command == 0:
            value=False
            break
               
        file_name= input("Please insert the name of the excel file: ")

        if command == 1:
            scheme.is_suspended(file_name)
        
        if command == 2:
            scheme.valid_licenses(file_name)

        if command == 3:
            scheme.find_by_category(file_name)
        
        time.sleep(2)

        if os.name == 'nt':
            os.system("cls")
        else:
            os.system('clear')  
        

if __name__ == '__main__':
    main()
