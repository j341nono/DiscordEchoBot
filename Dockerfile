FROM python:3.12-slim

RUN pip install uv

RUN apt-get update && apt-get install -y \
    git build-essential cmake python3 python3-pip wget curl \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/ggerganov/llama.cpp.git && \
    cd llama.cpp && mkdir build && cd build && \
    cmake .. && cmake --build . --config Release

WORKDIR /app

COPY . /app

RUN uv sync

CMD ["bash", "start.sh"]
