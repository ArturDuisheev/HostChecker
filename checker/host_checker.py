import os

import asyncio
import requests
import time
from dotenv import load_dotenv

from datetime import datetime
from telegram import Bot

load_dotenv()

SERVER_URL = os.getenv('SERVER_URL')
CHECK_INTERVAL = 30
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

bot = Bot(token=TELEGRAM_BOT_TOKEN)

def check_server():
    try:
        response = requests.get(SERVER_URL, timeout=5)
        response.raise_for_status()
        return True, None
    except Exception as e:
        return False, str(e)

def print_log(event):
    timestamp = datetime.now().strftime("%Y-%m-%d%H:%M:%S")
    with open(f'logs/c.log', 'a') as f:
        f.write(f"{timestamp}: {event}\n")

async def send_message(message):
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode='Markdown')

async def main():
    print("Running")
    while True:
        is_server_up, error_message = check_server()
        print(datetime.now(), "Server is up:", is_server_up)

        if not is_server_up:
            log_message = f"Server Shutdown: {error_message}"
            print(log_message)
            await send_message(f'Server Shutdown, смотрите логи: {error_message}')
            print_log(log_message)

        await asyncio.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())
