FROM python:3.12-slim

RUN pip install uv

RUN apt-get update && apt-get install -y \
    git build-essential wget curl \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/ggerganov/llama.cpp.git && \
    cd llama.cpp && make

WORKDIR /app

COPY . /app

RUN uv sync

CMD ["bash", "start.sh"]
