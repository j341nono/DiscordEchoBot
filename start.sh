#!/bin/bash

# at once
# bash model/download.sh　

# ./llama.cpp/server -m model/phi-2.Q4_K_M.gguf --port 8080 &

# uv run src/bot.py

uv run src/llama_server.py &
uv run src/bot.py