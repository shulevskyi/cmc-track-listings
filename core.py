import time
import telebot
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from datetime import datetime, timedelta, timezone
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
parameters = {
    'start': '1'
}

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '',
}

coinIDCurrent, coinIDPrevious = None, None

while True:

    session = Session()
    session.headers.update(headers)

    try:
        coinIDPrevious = coinIDCurrent

        response = session.get(url, params=parameters)
        data = json.loads(response.text)

        coinIDCurrent = data['data'][-1]['id']

        print(coinIDPrevious, coinIDCurrent)

        if coinIDPrevious is not None and coinIDCurrent > coinIDPrevious:
            if data['data'][-1]['platform'] is not None:
                if data['data'][-1]['platform']['symbol'] == 'BNB':

                    coinSymbolTelegram = data['data'][-1]['symbol']
                    coinStatusTelegram = data['data'][-1]['is_active']
                    coinPlatformTelegram = data['data'][-1]['platform']['name']
                    coinAddressTelegram = data['data'][-1]['platform']['token_address'].lower()
                    BaseUrl = f'https://matcha.xyz/markets/56/{coinAddressTelegram}'

                    bot_message = \
                        f'\U0001F7E1 New listing [{coinSymbolTelegram}] from CMC pro-database: \n \n' \
                        f'Token symbol: {coinSymbolTelegram} \n' \
                        f'Status: {coinStatusTelegram} \n' \
                        f'Address: {coinAddressTelegram} \n' \
                        f'Platform: {coinPlatformTelegram} \n' \
                        f'Time UTC: {str(datetime.now(timezone.utc))[0:19]} \n \n' \
                        f'Trade link: {BaseUrl}'

                    print('Sending to TG...')

                    bot = telebot.TeleBot('2137631648:AAHuZe5ewqF1nHXmrBaQ7RImux48L_aYor0')
                    user_id = [1944256295]

                    for chat in user_id:
                        bot.send_message(chat_id=chat, text=bot_message)

        time.sleep(30)

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
