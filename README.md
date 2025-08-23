# Discord-Echo-Bot

[日本語版はこちら / Japanese Version](README.ja.md)

A conversational bot for use on Discord.

This bot uses the mmnga/gemma-7b-it-q8_0.gguf model from Hugging Face. It supports both Japanese and English.

## Setup

```bash
./install.sh
```

Access the [Discord Developer Portal](https://discord.com/developers/) and select your application.

### 1. Enable Privileged Gateway Intents

Open the "Bot" tab from the left menu.

Turn on the "MESSAGE CONTENT INTENT" switch.

### 2. Generate Bot Invitation URL and Set Permissions

Generate a URL to invite the bot to your server.

Select "OAuth2" > "URL Generator" from the left menu.

Check "bot" in "SCOPES".

In the "BOT PERMISSIONS" displayed below, check the following permissions:

- View Channels
- Send Messages
- Read Message History

Copy the generated URL and access it in your browser to add the bot to your server.

## Usage

```bash
./start.sh
```

## Future Enhancements

- Implement streaming output
- Enable the use of past chat history
- Implement automatic deletion of old history when exceeding a certain character count