from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "PHA Diagnostics API is running"}
    
@app.get("/health")
def health():
    return {"status": "ok"}
