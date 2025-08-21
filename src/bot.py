import discord
import requests
import os

TOKEN = os.environ["DISCORD_BOT_TOKEN"]
LLAMA_API = "http://localhost:8080/completion"

intents = discord.Intents.default()
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
        prompt = message.content.replace(f"<@{client.user.id}>", "").strip()
        if not prompt:
            return

        payload = {
            "prompt": f"あなたは，非常に馴れ馴れしくフレンドリーな日本語のAIアシスタントです。\nユーザー: {prompt}\nアシスタント:",
            "n_predict": 256,
            "temperature": 0.7
        }

        try:
            response = requests.post(LLAMA_API, json=payload)
            text = response.json().get("content", "(Failed to respond)")
            await message.channel.send(text)
        except Exception as e:
            await message.channel.send(f"Error: {e}")

client.run(TOKEN)
