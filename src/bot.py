import discord
import requests
import os

TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
if TOKEN is None:
    raise RuntimeError("環境変数 DISCORD_BOT_TOKEN が設定されていません！")

LLAMA_API = "http://localhost:8080/completion"

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return
    
    if client.user in message.mentions:
        content = message.clean_content
        prompt = content.replace(f"@{client.user.name}", "").strip()
        if not prompt:
            return

        payload = {
            "prompt": f"あなたは非常に馴れ馴れしくフレンドリーな日本語のAIアシスタントです。\nユーザー: {prompt}\nアシスタント:",
            "n_predict": 256,
            "temperature": 0.7
        }

        try:
            response = requests.post(LLAMA_API, json=payload, timeout=60)
            data = response.json()
            if "content" in data and isinstance(data["content"], list):
                text = "".join([c.get("text", "") for c in data["content"]])
            else:
                text = "(No response from model)"
            await message.channel.send(text)
        except Exception as e:
            await message.channel.send(f"Error: {e}")

client.run(TOKEN)
