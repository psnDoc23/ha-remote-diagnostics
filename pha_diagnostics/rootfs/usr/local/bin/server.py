print("PHA Diagnostics server.py is running")
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/info")
def info():
    return {"message": "PHA Diagnostics API is running"}
