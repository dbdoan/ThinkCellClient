import os
import json
import requests

if os.name == "nt":
    os.system('cls')
else:
    os.system('clear')

# Input PPTTC file path
input_ppttc_path = r"C:\Users\dbdev\Documents\GitHub\ThinkCellClient\Backend\thinkcell-converter\ppttc_output.ppttc"

# Read key-file
with open(input_ppttc_path, "r", encoding="utf-8") as f:
    keyfile_contents = json.load(f)

# Replace all template url in PPTTC
TEMPLATE_URL = "http://127.0.0.1:8000/templates/template.pptx"

for slide in keyfile_contents:
    if "template" in slide:
        slide["template"] = TEMPLATE_URL

# Send to Thinkcell Server
server_url = "http://localhost:8080/"
headers = {
    "Content-Type": "application/vnd.think-cell.ppttc+json",
}

response = requests.post(server_url, headers=headers, json=keyfile_contents)


if response.status_code == 200:
    output_filename = os.path.basename(input_ppttc_path).replace('.ppttc', '.pptx')
    with open(output_filename, "wb") as f:
        f.write(response.content)
    print(f"✅ Received and saved {output_filename}!")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)


# # Serve static files under /templates
# app.mount("/templates", StaticFiles(directory="templates"), name="templates")

# # (Optional) Serve specific file if you want a direct route
# @app.get("/download-template")
# def download_template():
#     return FileResponse("templates/template.pptx", media_type='application/vnd.openxmlformats-officedocument.presentationml.presentation', filename="template.pptx")


# # Use absolute path to the "templates" folder
# template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "templates"))

# # Mount /templates so you can serve template.pptx
# app.mount("/templates", StaticFiles(directory=template_dir), name="templates")

# @app.get("/")
# def read_root():
#     return {"message": "FastAPI is running and serving templates."}
