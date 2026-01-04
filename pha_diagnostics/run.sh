#!/usr/bin/env sh
echo "PHA Diagnostics add-on started"
cd /usr/local/bin
exec python -m uvicorn server:app --host 0.0.0.0 --port 8000
