import telebot
from telebot import types
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from datetime import datetime, timezone
import time
from urllib.parse import urlencode
import requests

coinMaxIDCurrent, coinMaxIDPrevious = None, None

bot_token = '2115705864:AAFELUiqkPjO9Ndpod9CkVqJgiwYldMytUQ'
bot_chatID = ['2143580591', '941016072', '485492322']

while True:

    query_string = [
        ('start', '1'),
        ('limit', '10000'),
        ('convert', 'USD')
    ]
    base = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?"
    data = requests.get(f"{base}{urlencode(query_string)}").json()

    try:

        coinMaxIDPrevious = coinMaxIDCurrent
        coinAllID = []

        for i in data["data"]["cryptoCurrencyList"]:
            pass

        if coinMaxIDCurrent is not None:
            for i in data["data"]["cryptoCurrencyList"]:
                if i['id'] > coinMaxIDCurrent:
                    coinMaxIDCurrent = i['id']

        if coinMaxIDCurrent is None:
            for i in data["data"]["cryptoCurrencyList"]:
                coinAllID.append(i['id'])
            coinMaxIDCurrent = max(coinAllID)

        print(coinMaxIDPrevious, coinMaxIDCurrent, str(datetime.now(timezone.utc))[0:19])  # Test output for console

        for i, k in enumerate(data['data']['cryptoCurrencyList']):
            if k['id'] == coinMaxIDCurrent and coinMaxIDPrevious is not None:

                if coinMaxIDCurrent > coinMaxIDPrevious:
                    coinSymbolTelegram = k['symbol']
                    coinStatusTelegram = 'Active'
                    coinSlug = k['slug']

                    bot_message = \
                        f'\U0001F7E2 Token [{coinSymbolTelegram}] added to "Recently added" section on CMC: \n \n' \
                        f'Token symbol: {coinSymbolTelegram} \n' \
                        f'Status: {coinStatusTelegram} \n' \
                        f'Time UTC: {str(datetime.now(timezone.utc))[0:19]} \n \n' \

                    print('Sending to TG...', coinSymbolTelegram)

                    coinInfoUrl = f'https://coinmarketcap.com/currencies/{coinSlug}'
                    bot = telebot.TeleBot(token=bot_token)

                    markup_inline = types.InlineKeyboardMarkup()
                    coinInfo = types.InlineKeyboardButton(text='COINMARKETCAP', url=coinInfoUrl)

                    markup_inline.add(coinInfo)
                    
                    for users in bot_chatID:
                        bot.send_message(users, bot_message, reply_markup=markup_inline)

        time.sleep(5)

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
