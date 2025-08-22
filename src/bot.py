import discord
import requests
import os

TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
if TOKEN is None:
    raise RuntimeError("環境変数 DISCORD_BOT_TOKEN が設定されていません！")

LLAMA_API = "http://127.0.0.1:8080/completion"

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
        
        # 毎回このプロンプトでリセットされるので、会話の文脈は引き継ぎません
        prompt = f"あなたはフレンドリーな日本語のAIアシスタントです。次に示すユーザーの問いかけに対して、適切な返しをおこなってください。\nユーザー: {user_input}\nアシスタント:"
        
        # APIリクエストのペイロード
        payload = {
            "prompt": prompt,
            "max_tokens": 256,
            "temperature": 0.7,
            "repeat_penalty": 1.1,
            "stop": ["ユーザー:", "\n"]
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
                # このエラーが最も重要です
                await message.channel.send("ごめんなさい、AIサーバーに接続できませんでした。サーバーが起動しているか確認してください。")
            except requests.exceptions.RequestException as e:
                await message.channel.send(f"リクエスト中にエラーが発生しました: `{e}`")
            except Exception as e:
                await message.channel.send(f"予期せぬエラーが発生しました: `{e}`")

# ボットの実行
client.run(TOKEN)