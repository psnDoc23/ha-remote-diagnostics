from fastapi import FastAPI

app = FastAPI()
from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
        <body style="color: green; background: transparent;">
            <h1>PHA Resolve API is running</h1>
            <p>blah, blah, blah...</p>
        </body>
    </html>
    """
    
@app.get("/health")
def health():
    return {"status": "ok"}
