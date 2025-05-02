from collections import defaultdict
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

import csv
import json
import os
import subprocess


if os.name == "nt":
    os.system("cls")
else:
    os.system("clear")

load_dotenv()

vite_url = os.getenv("VITE_URL")
# print("vite_url loaded:", vite_url)

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
    
    # // template path
        
    template_dir = os.path.abspath("template")
    os.makedirs(template_dir, exist_ok=True)
    
    for filename in os.listdir(template_dir):
        template_file_path = os.path.join(template_dir, filename)
        os.remove(template_file_path)
    
    save_template_path = os.path.join(template_dir, templateFile.filename)
    
    # // key path
    key_dir = os.path.abspath('key')
    os.makedirs(key_dir, exist_ok=True)
    
    for filename in os.listdir(key_dir):
        key_file_path = os.path.join(key_dir, filename)
        os.remove(key_file_path)
        
    save_key_path = os.path.join(key_dir, keyFile.filename)
    
    try:
        content = await templateFile.read()
        with open(save_template_path, "wb") as file:
            file.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save template_file due to error: {e}")
    
    if key_ext == '.ppttc':
        print(key_ext)
        try:
            content = await keyFile.read()
            with open(save_key_path, "wb") as file:
                file.write(content)
        except:
         raise HTTPException(status_code=500, detail=f"Failed to save key_file due to error: {e}")    
    elif key_ext == '.csv':
        print(key_ext)
    
    json_contents = await keyFile.read()
    json_text = json_contents.decode('utf-8')
    return {"keyFile contents: ": json_text}

# [x] if key_file is ppttc, proceed with storing key into key folder 
# [ ] if key_file is csv, convert to ppttc before storign into key folder

# [x] either way, save the pptx template in template foolder

# then send both key and template file to the thinkcell server
# save output pptx to output folder and send that output back to user

@app.get("/")
def read_root():
    return {"Hello": "World"}