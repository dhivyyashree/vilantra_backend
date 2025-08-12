from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.routes import products, upload
import os
load_dotenv()

print("MONGO_URI:", os.getenv("MONGODB_URI"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router, prefix="/products")
app.include_router(upload.router, prefix="/upload")

@app.options("/upload/")
def options_upload():
    return {"message": "CORS preflight OK"}
@app.get("/ping")
def ping():
    return {"message": "pong"}