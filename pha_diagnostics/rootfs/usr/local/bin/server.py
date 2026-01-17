from fastapi import FastAPI
import httpx
import json
from pathlib import Path
import re

app = FastAPI()

ISSUES_PATH = Path("/data/issues.json")

# Load issues at startup
with ISSUES_PATH.open() as f:
    ISSUES = json.load(f)["issues"]


async def fetch_supervisor_logs():
    """
    Fetch Home Assistant Core logs from Supervisor API.
    The Supervisor injects the token into the container as an env var.
    """
    headers = {
        "Authorization": f"Bearer {Path('/data/supervisor_token').read_text().strip()}",
        "Content-Type": "application/json",
    }

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


@app.get("/diagnostics/run")
async def run_diagnostics():
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
