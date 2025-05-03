from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import json
import os
import requests
import shutil
import threading
import time

load_dotenv()
vite_local_url = os.getenv("VITE_LOCAL_URL")
vite_external_url = os.getenv("VITE_EXTERNAL_URL")
fastapi_external_url = os.getenv("FASTAPI_EXTERNAL_URL")
thinkcell_server_url = os.getenv("THINKCELL_SERVER_URL")

app = FastAPI()

# Allows requests from VITE server
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    vite_local_url,
    vite_external_url,
    "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "sessions"))
app.mount("/sessions", StaticFiles(directory=session_dir), name="sessions")

def send_to_thinkcell_server(keyfile_contents, uuid):
    headers = {"Content-Type": "application/vnd.think-cell.ppttc+json"}
    try:
        response = requests.post(thinkcell_server_url, headers=headers, json=keyfile_contents)
        print("Response status:", response.status_code)
        if response.status_code == 200:
            output_dir = os.path.abspath(os.path.join("sessions", uuid, "output"))
            os.makedirs(output_dir, exist_ok=True)
            output_filename = "output.pptx"
            output_path = os.path.join(output_dir, output_filename)
            
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"✅ Saved to: {output_path}")
        else:
            print("ThinkCell server error:")
            print(response.text)
    except Exception as e:
        print("Failed to contact ThinkCell server:", e)

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

    # Key path
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
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save key_file due to error: {e}")    
     
        # Now we can start the processing
        # Read key-file
        with open(save_key_path, "r", encoding="utf-8") as f:
            keyfile_contents = json.load(f)
            
        # Replace Template URL in PPTTC with proper
        TEMPLATE_URL = f"{fastapi_external_url}/sessions/{uuid}/template/template.pptx"
        for slide in keyfile_contents:
            if "template" in slide:
                slide["template"] = TEMPLATE_URL

        threading.Thread(target=send_to_thinkcell_server, args=(keyfile_contents, uuid)).start()
        
        output_url = f"{fastapi_external_url}/sessions/{uuid}/output/output.pptx"
        
        return {
            "message": "Files received and processing started",
            "url": output_url
            }

    elif key_ext == '.csv':
        return {"message": "CSV upload not implemented yet"}
    
def cleanup_sessions(max_live_hours=3, interval_checks_mins=30):
    while True:
        now = datetime.now()
        cutoff = now - timedelta(max_live_hours)
        
        for uuid_folder in os.listdir(session_dir):
            folder_path = os.path.join(session_dir, uuid_folder)
            if os.path.isdir(folder_path):
                last_modified = datetime.fromtimestamp(os.path.getmtime(folder_path))
                if last_modified < cutoff:
                    try:
                        shutil.rmtree(folder_path)
                        print(f"Deleted expired session folder: {folder_path}")
                    except Exception as e:
                        print(f"Error deleting folder {folder_path}: {e}")
        time.sleep(interval_checks_mins * 60)
        
threading.Thread(target=cleanup_sessions, daemon=True).start()

# To-Do
# [x] If key_file is ppttc, proceed with storing key into Key folder 
# [x] Either way, save the PPTX template in Template foolder
# [X] Then send both Key and Template file to the Thinkcell server
# [X} Save output PPTX to Output folder and send that output back to user

## Low Priority
# [ ] If key_file is a CSV, convert to PPTTC before storing into Key folder

@app.get("/")
def read_root():
    return {"Hello": "World"}