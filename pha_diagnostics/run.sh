#!/usr/bin/env bash
echo "PHA Diagnostics add-on started"
ls -l /usr/local/bin
python3 /usr/local/bin/server.py
echo "Python exited with code $?"
