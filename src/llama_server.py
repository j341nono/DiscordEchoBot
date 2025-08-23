import subprocess
import time
import sys
import os

def start_llama_server():
    cmd = [
        "./llama.cpp/build/bin/llama-server",
        "-m", "model/gemma-7b-it-q8_0.gguf",
        "--port", "8081",
        "--host", "0.0.0.0",  # 外部からのアクセスを許可
        "--ctx-size", "128",
        "--gpu-layers", "32"
    ]
    
    print("Starting llama server...")
    print(f"Command: {' '.join(cmd)}")

    try:
        process = subprocess.Popen(cmd)
        print(f"Llama server started with PID: {process.pid}")
        
        time.sleep(3)
        
        if process.poll() is None:
            print("Llama server is running successfully!")
            return process
        else:
            print("Llama server failed to start!")
            return None
            
    except Exception as e:
        print(f"Error starting llama server: {e}")
        return None

if __name__ == "__main__":
    server_process = start_llama_server()
    
    if server_process:
        try:
            server_process.wait()
        except KeyboardInterrupt:
            print("\nShutting down llama server...")
            server_process.terminate()
            server_process.wait()
            print("Llama server stopped.")