import os
import subprocess

os.system(
    "cls" if os.name == "nt" else "clear"
)

csv_path = "test_input\\input.csv"
ppttc_path = "test_input\\template.pptx"
pptx_output_path = "test_input\\output.pptx"

# 1. Take a CSV input and convert it to JSON structure

# 2. Take JSON and convert to PPTTC

# 3. Use CLI to call .exe and convert PPTTC to PPTX

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