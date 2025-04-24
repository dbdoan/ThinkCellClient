from collections import defaultdict
import csv
import json
import os
import subprocess

os.system(
    "cls" if os.name == "nt" else "clear"
)

input_csv_path = "test_input\\input.csv"
input_template_path = "test_input\\template.pptx"
ppttc_output_path = "ppttc_output.ppttc"
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

# # 1. Take a CSV input and convert it to JSON structure for PPTTC
def csv_to_json(data, ppttc_template):
    data = defaultdict(lambda: defaultdict(int), data)

    years = sorted(data.keys())
    series = sorted(set(type for year in data for type in data[year]))

    json_structure = {
        "template": ppttc_template,
        "data": [
            {
                "name": "Title",
                "table": [[{"string": "Slide #2"}]]
            },
            {
                "name": "Chart1",
                "table":
                [
                    # Header w/ years
                    [None] + 
                    [{"string": str(year)} for year in years],

                    # Empty row after header
                    []
                ] + [
                    [{"string": s}] + [{"number": data[year][s]}
                                                      for year in years]
                    for s in series
                ]
            }
        ]
    }
    return json.dumps([json_structure], indent=4)
# print(csv_to_json(data, input_template_path))

def run_thinkcell_cli(ppttc_file, output_pptx):
    command = [
        "C:\\Program Files (x86)\\think-cell\\ppttc.exe", ppttc_file, '-o', output_pptx
    ]

    try:
        result = subprocess.run(
            command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        print("Standard Output:", e.stdout)
        print("Standard Error:", e.stderr)

data = read_csv(input_csv_path)

# 2. Take JSON and convert to PPTTC
json_data_for_ppttc = csv_to_json(data, input_template_path)
with open(ppttc_output_path, 'w') as file:
    file.write(json_data_for_ppttc)

if __name__ == "__main__":
    # 3. Use CLI to call .exe and utilize PPTTC data + PPTX_template to PPTX
    run_thinkcell_cli(ppttc_output_path, pptx_output_path)