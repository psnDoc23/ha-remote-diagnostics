from fastapi import FastAPI

app = FastAPI()
from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
        <body style="color: red; background: transparent;">
            <h1>PHA Diagnostics API is running</h1>
        </body>
    </html>
    """
    
@app.get("/health")
def health():
    return {"status": "ok"}
