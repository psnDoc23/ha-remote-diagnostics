print("PHA Guardian loaded successfully")

from fastapi.responses import HTMLResponse
from fastapi import FastAPI
import httpx
import json
from pathlib import Path
import re

app = FastAPI()

ISSUES_PATH = Path("/data/issues.json")

# Load issues at startup
if ISSUES_PATH.exists():
    with ISSUES_PATH.open() as f:
        ISSUES = json.load(f)["issues"]
else:
    print("WARNING: /data/issues.json not found")
    ISSUES = []


async def fetch_supervisor_logs():
    """
    Fetch Home Assistant Core logs from Supervisor API.
    """
   

    token_path = Path("/data/supervisor_token")
    token = token_path.read_text().strip() if token_path.exists() else None

    print("Token exists:", token_path.exists())
    print("Token value:", repr(token))

    headers = {"Content-Type": "application/json"}

    # Only include Authorization header if token exists and is non-empty
    if token:
        headers["Authorization"] = f"Bearer {token}"

    async with httpx.AsyncClient() as client:
        resp = await client.get("http://supervisor/logs", headers=headers)
        resp.raise_for_status()
        return resp.text


def apply_rules_to_logs(issue, logs):
    """
    Apply all rules for a single issue to the log text.
    Returns (confidence, matches)
    """
    total_confidence = 0.0
    matches = []

    for rule in issue.get("rules", []):
        pattern = rule["pattern"]
        match_type = rule["match_type"]
        base_conf = rule.get("base_confidence", 0.0)

        # Match logic
        if match_type == "contains":
            if pattern.lower() in logs.lower():
                matches.append(pattern)
                total_confidence += base_conf

                # Apply confidence boosts
                for boost in rule.get("confidence_boosts", []):
                    cond = boost["condition"].replace("pattern: ", "").strip("'")
                    if cond.lower() in logs.lower():
                        total_confidence += boost["boost"]

        elif match_type == "regex":
            if re.search(pattern, logs, re.IGNORECASE):
                matches.append(pattern)
                total_confidence += base_conf

    return total_confidence, matches


@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
        <head>
            <title>PHA Guardian Diagnostics</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 40px;
                    background: #f5f5f5;
                }
                h1 {
                    color: #333;
                }
                button {
                    padding: 12px 20px;
                    font-size: 16px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    cursor: pointer;
                }
                button:hover {
                    background-color: #45a049;
                }
                #results {
                    margin-top: 30px;
                    padding: 20px;
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                pre {
                    white-space: pre-wrap;
                    word-wrap: break-word;
                }
            </style>
        </head>
        <body>
            <h1>PHA Guardian Diagnostics</h1>
            <p>Click the button below to run diagnostics.</p>

            <button onclick="runDiagnostics()">Run Diagnostics</button>

            <div id="results"></div>

            <script>
                async function runDiagnostics() {
                    const resultsDiv = document.getElementById("results");
                    resultsDiv.innerHTML = "<p><em>Running diagnostics...</em></p>";

                    try {
                        const resp = await fetch("./diagnostics/run");
                        const data = await resp.json();

                        resultsDiv.innerHTML = "<h2>Results</h2><pre>" +
                            JSON.stringify(data, null, 2) +
                            "</pre>";
                    } catch (err) {
                        resultsDiv.innerHTML = "<p style='color:red;'>Error running diagnostics.</p>";
                    }
                }
            </script>
        </body>
    </html>
    """


@app.get("/diagnostics/run")
async def run_diagnostics():

    print("Diagnostics endpoint hit")

    logs = await fetch_supervisor_logs()

    results = []

    for issue in ISSUES:
        confidence, matches = apply_rules_to_logs(issue, logs)

        if confidence > 0:
            results.append({
                "id": issue["id"],
                "name": issue["name"],
                "confidence": round(confidence, 3),
                "matches": matches,
                "resolution": issue["resolution"],
                "root_cause": issue["root_cause"]
            })

    return {"issues_detected": results}


@app.get("/health")
def health():
    return {"status": "ok"}
