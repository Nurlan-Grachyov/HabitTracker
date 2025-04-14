import requests

from config.settings import TG_URL, BOT_TOKEN


def send_tg_message(message, tg_id):
    params = {
        'text': message,
        'chat_id': tg_id,
    }
    requests.get(f'{TG_URL}{BOT_TOKEN}/sendMessage', params=params)
