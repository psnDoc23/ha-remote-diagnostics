@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
    <head>
        <title>PHA Resolve</title>
        <style>
            /* Force visibility regardless of HA theme */
            body {
                font-family: Arial, sans-serif;
                padding: 1.5rem;
                background: #f5f5f5 !important;   /* Light background */
                color: #222 !important;           /* Dark text */
            }

            .container {
                max-width: 700px;
                margin: auto;
                padding: 1.5rem;
                border-radius: 12px;
                background: #ffffff !important;   /* White card */
                color: #222 !important;           /* Dark text */
                border: 1px solid #ccc;
                box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            }

            h1, h2 {
                color: #1a4d8f !important;        /* Accent color */
                margin-top: 0;
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
                border: 1px solid #aaa;
                background: #fff !important;
                color: #222 !important;
            }

            .button {
                margin-top: 1rem;
                padding: 0.75rem 1.25rem;
                background: #1a73e8;
                color: white !important;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-size: 1rem;
            }

            .button:hover {
                background: #155fc0;
            }

            .consent-box {
                padding: 1rem;
                background: #eef3ff !important;
                border-radius: 8px;
                border: 1px solid #ccd8ff;
                margin-top: 0.5rem;
                color: #222 !important;
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
