from collections import defaultdict
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

import json
import os
import requests


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

session_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "sessions"))
app.mount("/sessions", StaticFiles(directory=session_dir), name="sessions")

@app.post("/upload/{uuid}/")
async def upload_files(uuid: str, keyFile: UploadFile = File(...), templateFile: UploadFile = File(...)):
    key_filename = keyFile.filename
    _, key_ext = os.path.splitext(key_filename.lower())

    # Testing session-based.
    template_dir = os.path.abspath(os.path.join("sessions", uuid, "template"))
    os.makedirs(template_dir, exist_ok=True)

    # Clear old files in session-specific template dir
    for filename in os.listdir(template_dir):
        template_file_path = os.path.join(template_dir, filename)
        os.remove(template_file_path)

    save_template_path = os.path.join(template_dir, "template.pptx")

    # // Key path
    key_dir = os.path.abspath(os.path.join("sessions", uuid, "key"))
    os.makedirs(key_dir, exist_ok=True)

    # Clear old key files
    for filename in os.listdir(key_dir):
        os.remove(os.path.join(key_dir, filename))

    save_key_path = os.path.join(key_dir, "key.ppttc")
    
    # Save the template file to the template dir
    try:
        content = await templateFile.read()
        with open(save_template_path, "wb") as file:
            file.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save template_file due to error: {e}")
    
    if key_ext == '.ppttc':
        try:
            content = await keyFile.read()
            with open(save_key_path, "wb") as file:
                file.write(content)
        except:
         raise HTTPException(status_code=500, detail=f"Failed to save key_file due to error: {e}")    
     
        # Now we can start the processing
        # Input PPTTC file path
        input_ppttc_path = os.path.join(key_dir, "key.ppttc")

        # Read key-file
        with open(input_ppttc_path, "r", encoding="utf-8") as f:
            keyfile_contents = json.load(f)
            
        # Replace all template url in PPTTC
        # TEMPLATE_URL = f"http://192.168.1.104:8000/sessions/{uuid}/template/template.pptx"
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
            output_dir = os.path.abspath(os.path.join("sessions", uuid, "output"))
            os.makedirs(output_dir, exist_ok=True)
            output_filename = "output.pptx"
            output_path = os.path.join(output_dir, output_filename)
            
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"✅ Received and saved {output_filename}!")
            
            output_url = f"http://192.168.1.104:8000/sessions/{uuid}/output/output.pptx"
            
            return {"message": "Success",
                    "file": os.path.basename(output_path),
                    "url": output_url}
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