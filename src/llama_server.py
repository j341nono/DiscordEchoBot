import subprocess

def start_llama_server():
    cmd = [
        "./llama.cpp/server",
        "-m", "model/gemma-7b-it-q4_0.gguf",
        "--port", "8080",
        "--ctx-size", "4096"
    ]
    subprocess.Popen(cmd)

if __name__ == "__main__":
    start_llama_server()
