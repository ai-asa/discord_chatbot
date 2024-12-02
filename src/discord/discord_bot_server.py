# %%
from dotenv import load_dotenv
import discord
import logging
import os

load_dotenv()

def start_discord_bot(flag_discord_comment_send,flag_discord_comment_receive):
    logging.basicConfig(filename='./log/subprocces_discord.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
    
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    TARGET_CHANNEL_ID = int(os.getenv('TARGET_CHANNEL_ID'))

    # Intentsを設定
    intents = discord.Intents.all()  # イベントをすべて有効にする
    client = discord.Client(intents=intents)

    # 起動時に動作する処理
    @client.event
    async def on_ready():
        print('ログインしました')

    # メッセージ受信時に動作する処理
    @client.event
    async def on_message(message):
        try:
            logging.info("処理の入り")
            if message.author.bot:
                return
            if message.channel.id == TARGET_CHANNEL_ID:
                listener_name = message.author.display_name
                listener_comment = message.content
                flag_discord_comment_receive.put((listener_name,listener_comment))
                response = flag_discord_comment_send.get()
                if response != 0:
                    logging.info("response: %s", response)
                    await message.channel.send(response)
                logging.info("0のとき")
                return
        except Exception as e:
            # エラーをログに記録
            logging.error("An error occurred in subprocess_discord: %s", e)

    # Botの起動とDiscordサーバーへの接続
    client.run(DISCORD_TOKEN)

if __name__ == "__main__":
    start_discord_bot()
# %%
