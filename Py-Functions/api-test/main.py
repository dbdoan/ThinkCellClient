from os import system
if system == "nt":
    
    system("cls")
else:
    system("clear")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

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

@app.get("/user/{uuid}")
def read_uuid(uuid: str):
    return {"user id: ": uuid}