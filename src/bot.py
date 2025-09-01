import discord
import requests
import os
from transformers import AutoTokenizer

TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
if TOKEN is None:
    raise RuntimeError("環境変数 DISCORD_BOT_TOKEN が設定されていません！")

LLAMA_API = "http://127.0.0.1:8081/completion"
model_path = "model/gemma-7b-it-q8_0.gguf"


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
        user_input = message.clean_content.replace(f"@{client.user.name}", "").strip()
        
        if not user_input:
            await message.channel.send("呼びましたか？何かお話ししましょう！")
            return
        
        tokenizer = AutoTokenizer.from_pretrained("google/gemma-7b-it")

        chat = [
            # { "role": "system", "content": "あなたは日本語のカウンセラーです。以下のユーザーの入力分に対して、適切な返事をしてください。" },
            { "role": "user", "content": {user_input} },
        ]
        prompt = tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)


        # prompt = "<|im_start|>system\nあなたは日本語のカウンセラーです。以下のユーザーの入力分に対して、適切な返事をしてください。<|im_end|>"
        # prompt += f"<|im_start|>user\n{user_input}<|im_end|>"
        # prompt += "<|im_start|>assistan\n"
        
        # APIリクエストのペイロード
        payload = {
            "prompt": prompt,
            "max_tokens": 128,
            "temperature": 0.7,
            "repeat_penalty": 1.1,
            "stop": ["<|im_end|>"]
        }
        
        async with message.channel.typing():
            try:
                # AIモデルにリクエストを送信
                response = requests.post(LLAMA_API, json=payload, timeout=90)
                response.raise_for_status()
                
                data = response.json()
                ai_response = data.get("content", "").strip()
                
                if not ai_response:
                    ai_response = "うーん、うまく言葉が出てきません…。"
                
                await message.channel.send(ai_response)

            except requests.exceptions.ConnectionError:
                await message.channel.send("⚠️ AIサーバーに接続できませんでした。サーバーが起動しているか確認してください。")
            except requests.exceptions.Timeout:
                await message.channel.send("⚠️ 応答がタイムアウトしました。しばらくしてからもう一度試してください。")
            except requests.exceptions.RequestException:
                await message.channel.send("⚠️ リクエスト中にエラーが発生しました。サーバーの状態を確認してください。")
            except Exception:
                await message.channel.send("⚠️ 予期せぬエラーが発生しました。管理者に確認してください。")


client.run(TOKEN)