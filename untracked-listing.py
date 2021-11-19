import keep_alive
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from datetime import datetime, timedelta, timezone
import time
import requests

keep_alive.keep_alive()

coinMaxIDCurrent, coinMaxIDPrevious = None, None

# Telegram bot configuration
bot_token = '2137631648:AAHuZe5ewqF1nHXmrBaQ7RImux48L_aYor0'
bot_chatID = '1944256295'

while True:

    url = 'https://api.coinmarketcap.com/data-api/v3/map/all?listing_status=active,untracked'
    session = Session()

    try:

        coinMaxIDPrevious = coinMaxIDCurrent
        coinAllID = []

        response = session.get(url)
        data = json.loads(response.text)

        for i in data['data']['cryptoCurrencyMap']:
            coinAllID.append(i['id'])

        # Finding the max id that occurred in CMC web api. Simply, latest untracked listing
        coinMaxIDCurrent = max(coinAllID)
        print(coinMaxIDPrevious, coinMaxIDCurrent, str(datetime.now(timezone.utc))[0:19])  # Test output for console

        if coinMaxIDPrevious is not None:
            if coinMaxIDCurrent < coinMaxIDPrevious:
                coinMaxIDCurrent = coinMaxIDPrevious
                print('Token goes to active status, ID has been changed..')

        for i, k in enumerate(data['data']['cryptoCurrencyMap']):
            if k.get('platform') is not None:
                if k['id'] == coinMaxIDCurrent and coinMaxIDPrevious is not None:

                    if coinMaxIDCurrent > coinMaxIDPrevious:
                        coinSymbolTelegram = k['symbol']
                        coinStatusTelegram = k['status']
                        coinPlatformTelegram = k['platform']['name']
                        coinAddressTelegram = k['platform']['token_address'].lower()
                        # BaseUrl = f'https://matcha.xyz/markets/56/{coinAddressTelegram}'

                        bot_message = \
                            f'\U0001F7E1 New listing [{coinSymbolTelegram}] from CMC web-database v3 (Untracked): \n \n' \
                            f'Token symbol: {coinSymbolTelegram} \n' \
                            f'Status: {coinStatusTelegram} \n' \
                            f'Address: {coinAddressTelegram} \n' \
                            f'Platform: {coinPlatformTelegram} \n' \
                            f'Time UTC: {str(datetime.now(timezone.utc))[0:19]} \n \n' \
                            # f'Trade link: {BaseUrl}'

                        print('Sending to TG...')
                        print(coinSymbolTelegram)

                        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
                        response = requests.get(send_text)

        # CMC does not require api key for any operation on its web-api, thus, we may set any time here.
        time.sleep(5)

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
