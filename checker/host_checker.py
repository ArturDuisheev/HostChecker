import os
import asyncio
import requests
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
        return True
    except Exception as e:
        return False, str(e)

def print_log(event):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(f'logs/c.log', 'a') as f:
        f.write(f"{timestamp}: {event}\n")

async def send_message(message):
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode='Markdown')

async def main():
    print("Running")
    prev_error_message = None
    error_count = 0
    
    while True:
        is_server_up, error_message = check_server()
        print(datetime.now(), "Server is up:", is_server_up)

        if not is_server_up:
            error_count += 1
            log_message = f"Server Shutdown: {error_count} consecutive errors"
            
            if error_count >= 5:
                break
            
            # Проверяем, является ли текущая ошибка такой же, как предыдущая
            if error_message == prev_error_message:
                log_message += " (same error)"
            else:
                log_message += f" (new error: {error_message})"
            
            print(log_message)
            await send_message(f'Server Shutdown, смотрите логи: {log_message}')
            print_log(log_message)

            prev_error_message = error_message

        await asyncio.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())
