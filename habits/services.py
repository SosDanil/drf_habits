import requests

from config.settings import TELEGRAM_URL, TELEGRAM_BOT_TOKEN


def send_telegram_message(chat_id, message):
    params = {
        'chat_id': chat_id,
        'message': message
    }
    requests.get(f'{TELEGRAM_URL}{TELEGRAM_BOT_TOKEN}/sendMessage', params=params)


send_telegram_message(1710780709, 'Hi!')
