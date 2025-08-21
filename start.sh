#!/bin/bash
bash model/download.sh

./llama.cpp/server -m model/phi-2.Q4_K_M.gguf --port 8080 &

uv run src/bot.py
