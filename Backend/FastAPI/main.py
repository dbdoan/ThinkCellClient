from collections import defaultdict
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from pathlib import Path

import csv
import json
import os
import requests
import subprocess


if os.name == "nt":
    os.system("cls")
else:
    os.system("clear")

load_dotenv()

vite_url = os.getenv("VITE_URL")
app = FastAPI()

# Allows requests from VITE server
app.add_middleware(
    CORSMiddleware,
    allow_origins=[vite_url, "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "template"))
app.mount("/template", StaticFiles(directory=template_dir), name="template")

key_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "key"))
app.mount("/key", StaticFiles(directory=key_dir), name="key")

@app.post("/upload/{uuid}/")
async def upload_files(uuid: str, keyFile: UploadFile = File(...), templateFile: UploadFile = File(...)):
    key_filename = keyFile.filename
    _, key_ext = os.path.splitext(key_filename.lower())
    
    # // Template path
    template_dir = os.path.abspath("template")
    os.makedirs(template_dir, exist_ok=True)
    
    for filename in os.listdir(template_dir):
        template_file_path = os.path.join(template_dir, filename)
        os.remove(template_file_path)

    save_template_path = os.path.join(template_dir, "template.pptx")

    # // Key path
    key_dir = os.path.abspath('key')
    os.makedirs(key_dir, exist_ok=True)
    
    for filename in os.listdir(key_dir):
        key_file_path = os.path.join(key_dir, filename)
        os.remove(key_file_path)
        
    save_key_path = os.path.join(key_dir, "key.ppttc")
    
    # Save the template file to the template dir
    try:
        content = await templateFile.read()
        with open(save_template_path, "wb") as file:
            file.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save template_file due to error: {e}")
    
    if key_ext == '.ppttc':
        
        # Save the key file to the key dir
        try:
            content = await keyFile.read()
            with open(save_key_path, "wb") as file:
                file.write(content)
        except:
         raise HTTPException(status_code=500, detail=f"Failed to save key_file due to error: {e}")    
     
        # Now we can start the processing
        # Input PPTTC file path
        input_ppttc_path = Path.home() / "Documents" / "Github" / "ThinkCellClient" / "Backend" / "FastAPI" / "key" / "key.ppttc"
        
        # Read key-file
        with open(input_ppttc_path, "r", encoding="utf-8") as f:
            keyfile_contents = json.load(f)
            
        # Replace all template url in PPTTC
        TEMPLATE_URL = "http://192.168.1.104:8000/template/template.pptx"

        for slide in keyfile_contents:
            if "template" in slide:
                slide["template"] = TEMPLATE_URL
                
                
        # Send to Thinkcell Server
        server_url = "http://108.198.175.239:8080/"
        headers = {
            "Content-Type": "application/vnd.think-cell.ppttc+json",
        }

        response = requests.post(server_url, headers=headers, json=keyfile_contents)
        
        if response.status_code == 200:
            
            output_dir = Path(__file__).parent / "output"
            output_dir.mkdir(exist_ok=True)
            
            output_filename = os.path.basename(input_ppttc_path).replace('.ppttc', '.pptx')
            
            output_path = output_dir / output_filename
            
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"✅ Received and saved {output_filename}!")
            
            return {"message": "Success", "file": str(output_path.name)}
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)

    elif key_ext == '.csv':
        print(key_ext)
        
# [x] if key_file is ppttc, proceed with storing key into key folder 
# [ ] if key_file is csv, convert to ppttc before storing into key folder
# [x] either way, save the pptx template in template foolder
# then send both key and template file to the thinkcell server
# save output pptx to output folder and send that output back to user

@app.get("/")
def read_root():
    return {"Hello": "World"}