#!/usr/bin/env sh
echo "PHA Diagnostics add-on started"
cd /usr/local/bin
exec /venv/bin/python -m uvicorn server:app --host 0.0.0.0 --port 8099
# exec python -m uvicorn server:app --host 0.0.0.0 --port 8099
