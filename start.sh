#!/bin/bash

export CUDA_VISIBLE_DEVICES=0

# ./llama.cpp/server -m model/phi-2.Q4_K_M.gguf --port 8080 &

uv run src/llama_server.py & uv run src/bot.py
