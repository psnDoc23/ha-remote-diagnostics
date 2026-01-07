from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
    <head>
        <title>PHA Resolve</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                padding: 1.5rem;
                color: var(--primary-text-color);
                background: var(--card-background-color);
            }
            .container {
                max-width: 700px;
                margin: auto;
                padding: 1.5rem;
                border-radius: 12px;
                background: var(--ha-card-background, rgba(255,255,255,0.05));
                box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            }
            h1 {
                margin-top: 0;
                font-size: 1.8rem;
                color: var(--primary-color);
            }
            .section {
                margin-top: 1.5rem;
            }
            label {
                font-weight: bold;
                display: block;
                margin-bottom: 0.5rem;
            }
            textarea {
                width: 100%;
                height: 120px;
                padding: 0.75rem;
                border-radius: 8px;
                border: 1px solid var(--divider-color);
                background: var(--input-background-color, rgba(0,0,0,0.1));
                color: var(--primary-text-color);
            }
            .button {
                margin-top: 1rem;
                padding: 0.75rem 1.25rem;
                background: var(--primary-color);
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-size: 1rem;
            }
            .button:hover {
                opacity: 0.9;
            }
            .consent-box {
                padding: 1rem;
                background: rgba(0,0,0,0.1);
                border-radius: 8px;
                margin-top: 0.5rem;
            }
        </style>
    </head>

    <body>
        <div class="container">
            <h1>PHA Resolve</h1>
            <p>Your Home Assistant diagnostics companion.</p>

            <div class="section">
                <h2>Access & Permissions</h2>
                <p>PHA Resolve can analyze your configuration, logs, and system state to help identify issues and build a baseline for future troubleshooting.</p>

                <div class="consent-box">
                    <label>
                        <input type="checkbox" id="consent">
                        I allow PHA Resolve to read my Home Assistant logs and configuration for diagnostic purposes.
                    </label>
                </div>
            </div>

            <div class="section">
                <h2>Describe the Issue</h2>
                <p>If you're experiencing a problem, tell us what’s going on. This will be included in the diagnostic review.</p>

                <label for="issue">What seems to be happening?</label>
                <textarea id="issue" placeholder="Example: Automations stopped running after the last update..."></textarea>

                <button class="button" onclick="submitDiagnostics()">Submit</button>
            </div>

            <div class="section" id="result"></div>
        </div>

        <script>
            function submitDiagnostics() {
                const consent = document.getElementById('consent').checked;
                const issue = document.getElementById('issue').value;

                document.getElementById('result').innerHTML = `
                    <p><strong>Consent:</strong> ${consent ? "Granted" : "Not granted"}</p>
                    <p><strong>Issue Description:</strong> ${issue || "No description provided"}</p>
                    <p>This will eventually be sent to the PHA Resolve API for analysis.</p>
                `;
            }
        </script>
    </body>
    </html>
    """
