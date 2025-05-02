from collections import defaultdict
import csv
import json
import os
import subprocess

if os.name == "nt":
    os.system('cls')
else:
    os.system('clear')
    
input_csv = "/Users/danny/Documents/GitHub/ThinkCellClient/Functionality-Framing/thinkcell-converter/input.csv"
    
def read_csv(csv_file):
    data = {}
    
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        key_column = fieldnames[0]

        for row in reader:
            cell_A1 = row.pop(key_column)
            data[cell_A1] = {series_num: int(count)
                          for series_num, count in row.items()}
    return data

print(read_csv(input_csv))