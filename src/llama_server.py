import subprocess

def start_llama_server():
    cmd = [
        "./llama.cpp/server",
        "-m", "model/phi-2.Q4_K_M.gguf",
        "--port", "8080"
    ]
    subprocess.Popen(cmd)

if __name__ == "__main__":
    start_llama_server()
