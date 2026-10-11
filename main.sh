#!/bin/bash
echo 'starting'
uv run src/main.py
cd public && python3 -m http.server 8888
