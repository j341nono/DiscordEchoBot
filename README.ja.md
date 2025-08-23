# Discord-Echo-Bot

[English Version](README.md)

Discord上で使用可能な対話Botです。

Hugging Face の mmnga/gemma-7b-it-q8_0.gguf のモデルを使用します。日本語と英語に対応しています。

## セットアップ

```bash
./install.sh
```

[Discord Developer Portal](https://discord.com/developers/)にアクセスし、あなたのアプリケーションを選択します。

### 1. 特権ゲートウェイインテントの有効化

左側のメニューから「Bot」タブを開きます。

「MESSAGE CONTENT INTENT」のスイッチをオンにしてください。

### 2. ボットの招待URL生成と権限設定

ボットをあなたのサーバーに招待するためのURLを生成します。

左側のメニューから「OAuth2」>「URL Generator」を選択します。

「SCOPES」で bot にチェックを入れます。

下に表示される「BOT PERMISSIONS」で、以下の権限にチェックを入れてください。

- チャンネルを見る（View Channels）
- メッセージを送信（Send Messages）
- メッセージ履歴を読む（Read Message History）

生成されたURLをコピーし、ブラウザでアクセスしてボットをサーバーに追加します。

## 実行

```bash
./start.sh
```

## 今後の拡張性

- ストリーミング出力を実装する
- 過去のチャット履歴を使用できるようにする
- 特定の文字数以上になったら、古い履歴を順に削除するようにしたい