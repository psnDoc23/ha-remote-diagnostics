#!/usr/bin/env sh
echo "PHA Guardian Diagnostic add-on started"
cd /usr/local/bin
# per cop 20260117 changing back to 8000 because ingress is in place
# exec /venv/bin/python -m uvicorn server:app --host 0.0.0.0 --port 8099
exec /venv/bin/python -m uvicorn server:app --host 0.0.0.0 --port 8000
# exec python -m uvicorn server:app --host 0.0.0.0 --port 8099
