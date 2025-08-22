#!/bin/bash

set -e

echo "Discord-Echo-Bot セットアップを開始します"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' 

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_requirements() {
    log_info "システム要件をチェック中..."

    # CUDA チェック
    if ! command -v nvidia-smi &> /dev/null; then
        log_error "nvidia-smi が見つかりません。CUDAがインストールされているか確認してください。"
        exit 1
    fi

    # CMake チェック
    if ! command -v cmake &> /dev/null; then
        log_error "cmake が見つかりません。インストールしてください: sudo apt install cmake"
        exit 1
    fi

    # Make チェック
    if ! command -v make &> /dev/null; then
        log_error "make が見つかりません。インストールしてください: sudo apt install build-essential"
        exit 1
    fi

    # Python チェック
    if ! command -v python3 &> /dev/null; then
        log_error "python3 が見つかりません。Pythonをインストールしてください。"
        exit 1
    fi

    # uv チェック
    if ! command -v uv &> /dev/null; then
        log_error "uv が見つかりません。uvをインストールしてください"
        exit 1
    fi

    log_info "システム要件チェック完了 ✓"
}

setup_llama_cpp() {
    log_info "llama.cpp をセットアップ中..."
    
    if [ ! -d "llama.cpp" ]; then
        log_info "llama.cpp をクローン中..."
        git clone https://github.com/ggerganov/llama.cpp.git
    else
        log_info "llama.cpp は既に存在します。更新中..."
        cd llama.cpp
        git pull
        cd ..
    fi
    
    cd llama.cpp
    
    if [ -d "build" ]; then
        log_info "既存のビルドディレクトリをクリア中..."
        rm -rf build
    fi
    
    mkdir build
    cd build
    
    log_info "CUDA対応でCMakeを実行中..."
    cmake .. -DGGML_CUDA=ON -DCMAKE_BUILD_TYPE=Release -DLLAMA_CURL=OFF
    
    log_info "コンパイル中（時間がかかる場合があります）..."
    make -j$(nproc)
    
    # バイナリが生成されたか確認
    if [ ! -f "bin/llama-server" ]; then
        log_error "llama-server バイナリが生成されませんでした。"
        exit 1
    fi
    
    log_info "llama.cpp ビルド完了 ✓"
    cd ../..
}

install_python_dependencies() {
    uv sync
}

setup_model_directory() {
    MODEL_FILE="model/gemma-7b-it-q4_0.gguf"

    if [ ! -f "$MODEL_FILE" ]; then
    echo "モデルファイル ($MODEL_FILE) のダウンロードを開始します..."
    
    mkdir -p model
    cd model
    wget https://huggingface.co/mmnga/gemma-7b-it-gguf/resolve/main/gemma-7b-it-q4_0.gguf
    cd ..

    fi
}


main() {
    echo "作業ディレクトリ: $(pwd)"
    echo ""
    
    check_requirements
    setup_llama_cpp
    install_python_dependencies
    setup_model_directory

    echo ""
    echo "============================================"
    log_info "セットアップが完了しました！"
    echo "============================================"
    echo ""
    echo "次の手順を実行してください:"
    echo ""
    echo "1. Discord Bot トークンを設定:"
    echo "   export DISCORD_BOT_TOKEN='your_token_here'"
    echo ""
    echo "2. Bot を起動:"
    echo "   ./start.sh"
    echo ""
    echo "============================================"
}


main "$@"