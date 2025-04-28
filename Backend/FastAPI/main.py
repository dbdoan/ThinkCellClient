from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

if os.system == "nt":
    os.system("cls")
else:
    os.system("clear")

load_dotenv()

vite_url = os.getenv("VITE_URL")

app = FastAPI()

# Allows requests from VITE server
app.add_middleware(
    CORSMiddleware,
    allow_origins=[vite_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

# @app.get("/user/{uuid}")
# def read_uuid(uuid: str):
#     return {"user id: ": uuid}

@app.post("/upload/{uuid}/")
async def upload_files(uuid: str, keyFile: UploadFile = File(...), templateFile: UploadFile = File(...)):
    
    json_contents = await keyFile.read()
    json_text = json_contents.decode('utf-8')
    
    # return {
    #     "userID: ": uuid,
    #     "keyFile: ": keyFile.filename,
    #     "templateFile: ": templateFile.filename,
    # }
    
    return {"keyFile contents: ": json_text}