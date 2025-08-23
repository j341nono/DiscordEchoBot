FROM nvidia/cuda:12.2.2-devel-ubuntu22.04

RUN apt-get update && apt-get install -y \
    git build-essential cmake python3 python3-pip wget curl \
    libcurl4-openssl-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv

RUN git clone https://github.com/ggerganov/llama.cpp.git && \
    cd llama.cpp && mkdir build && cd build && \
    cmake .. -DLLAMA_CUBLAS=ON && cmake --build . --config Release

WORKDIR /app
COPY . /app

RUN uv sync

CMD ["bash", "start.sh"]
