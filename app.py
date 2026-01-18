from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Phishing URL Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow chrome extension
    allow_credentials=True,
    allow_methods=["*"],   # allow POST, OPTIONS
    allow_headers=["*"],
)

# Load model once at startup
classifier = pipeline(
    "text-classification",
    model="ealvaradob/bert-finetuned-phishing",
    device=-1
)

class URLRequest(BaseModel):
    url: str

@app.get("/")
def health_check():
    return {"status": "API is running"}

@app.post("/check")
def check_phishing(data: URLRequest):
    result = classifier(data.url)[0]
    return {
        "url": data.url,
        "label": result["label"],
        "confidence": round(result["score"], 4)
    }
