from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

if os.name == "nt":
    os.system("cls")
else:
    os.system("clear")

load_dotenv()

vite_url = os.getenv("VITE_URL")
print("vite_url loaded:", vite_url)


app = FastAPI()

# Allows requests from VITE server
app.add_middleware(
    CORSMiddleware,
    allow_origins=[vite_url, "http://127.0.0.1:5173"],
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


# if file is ppttc, proceed with storing (temp)
# if file is csv, convert to ppttc

# either way, save the pptx template in temp

# then convert the ppttc key to pptx output
# return to user in root 