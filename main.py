from collections import defaultdict
import csv
import os
import subprocess

os.system(
    "cls" if os.name == "nt" else "clear"
)

input_csv_path = "test_input\\input.csv"
input_template_path = "test_input\\template.pptx"
ppttc_output_path = "test\\input\\ppttc_output.ppttc"
pptx_output_path = "test_input\\output.pptx"

def read_csv(csv_file):
    data = {}
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            year = row.pop('Year')
            data[year] = {series_num: int(count)
                          for series_num, count in row.items()}
            # print(row.items())
    return data

data = read_csv(input_csv_path)

# # 1. Take a CSV input and convert it to JSON structure
def csv_to_json(data, ppttc_template):
    data = defaultdict(lambda: defaultdict(int), data)

    years = sorted(data.keys())

    print(years)
    
    
csv_to_json(data, input_template_path)



# csv_to_json(test_csv, input_template_path)
# 2. Take JSON and convert to PPTTC

# 3. Use CLI to call .exe and utilize PPTTC data + PPTX_template to PPTX

# def run_thinkcell_cli(ppttc_file, output_pptx):
#     command = [
#         "C:\\Program Files (x86)\\think-cell\\ppttc.exe", ppttc_file, '-o', output_pptx]

#     # Execute the command using subprocess.
#     try:
#         result = subprocess.run(
#             command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#         print("think-cell processing successful.")
#     except subprocess.CalledProcessError as e:
#         print("Error:", e)
#         print("Standard Output:", e.stdout)
#         print("Standard Error:", e.stderr)

# if __name__ == "__main__":
#     print("test")