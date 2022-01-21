import json
from API.settings import env
import requests

def send_message(message:str, chat_id:int, keyboard:str):
    # print(keyboard_button)
    data = {
      "chat_id": chat_id,
      "text": message,
      "parse_mode": "MarkdownV2",
      "reply_markup": (None, keyboard)
    }
    response = requests.post(
      f"{env('TELEGRAM_URL')}{env('BOT_TOKEN')}/sendMessage", data=data
    )    
    # response.json()