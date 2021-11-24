import telebot
from telebot import types
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from datetime import datetime, timedelta, timezone
import time
coinMaxIDCurrent, coinMaxIDPrevious = None, None

bot_token = '2137631648:AAHuZe5ewqF1nHXmrBaQ7RImux48L_aYor0'
bot_chatID = ['1944256295', '941016072', '485492322']

while True:

    url = 'https://api.coinmarketcap.com/data-api/v3/map/all?listing_status=active'
    session = Session()
    
    try:
        
        coinMaxIDPrevious = coinMaxIDCurrent
        coinAllID = []
        
        response = session.get(url)
        data = json.loads(response.text)
        
        if coinMaxIDCurrent is not None:
            for i in data['data']['cryptoCurrencyMap']:
                if i['id'] > coinMaxIDCurrent:
                    coinMaxIDCurrent = i['id']
                    
        if coinMaxIDCurrent is None:
            for i in data['data']['cryptoCurrencyMap']:
                coinAllID.append(i['id'])
            coinMaxIDCurrent = max(coinAllID)
            
        print(coinMaxIDPrevious, coinMaxIDCurrent, str(datetime.now(timezone.utc))[0:19])  # Test output for console
        
        for i, k in enumerate(data['data']['cryptoCurrencyMap']):
            if k['id'] == coinMaxIDCurrent and coinMaxIDPrevious is not None:
                if k.get('platform') is not None:
                    
                    if coinMaxIDCurrent > coinMaxIDPrevious:
                        coinSymbolTelegram = k['symbol']
                        coinStatusTelegram = k['status']
                        coinPlatformTelegram = k['platform']['name']
                        coinAddressTelegram = k['platform']['token_address'].lower()
                        coinSlug = k['slug']
                        
                        bot_message = \
                            f'\U0001F7E0 Token [{coinSymbolTelegram}] appeared in CMC web-database v3 (Active): \n \n' \
                            f'Token symbol: {coinSymbolTelegram} \n' \
                            f'Status: {coinStatusTelegram} \n' \
                            f'Address: {coinAddressTelegram} \n' \
                            f'Platform: {coinPlatformTelegram} \n \n' \
                            f'Time UTC: {str(datetime.now(timezone.utc))[0:19]} \n \n' \

                        print('Sending to TG...', coinSymbolTelegram)
                        
                        coinInfoUrl = f'https://coinmarketcap.com/currencies/{coinSlug}'
                        coinExchangeUrl = f'https://poocoin.app/tokens/{coinAddressTelegram}'
                        
                        bot = telebot.TeleBot(token=bot_token)
                        
                        markup_inline = types.InlineKeyboardMarkup()
                        
                        coinInfo = types.InlineKeyboardButton(text='COINMARKETCAP', url=coinInfoUrl)
                        coinExchange = types.InlineKeyboardButton(text='POOCOIN', url=coinExchangeUrl)
                        
                        markup_inline.add(coinInfo, coinExchange)
                        bot.send_message(1944256295, bot_message, reply_markup=markup_inline)
                        
        time.sleep(5)
        
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
