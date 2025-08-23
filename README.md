# Dicord-Echo-Bot

Dicord上で使用可能な対話Botです．

Huggingface の mmnga/gemma-7b-it-q8_0.gguf のモデルを使用します．日本語と英語に対応しています．

# セットアップ

```bash
./install.sh
```

# 今後の拡張性

- ストリーミング出力を実装する．
- 過去のチャット履歴を使用できるようにする
    - 特定の文字数以上になったら，古い履歴を順に削除するようにしたい