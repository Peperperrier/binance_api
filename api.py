import os
import binance
import time
import datetime
import requests

from binance.client import Client

# init
api_key       = os.environ.get('binance_api')
api_secret    = os.environ.get('binance_secret')
# api_key         = '6ytIfpHV3E2s8tD15IR8o1c9eI9tW5kiDgehCj4eoFpWbSVN9u6Ca55DKdf5NrDK'
# api_secret      = 'EvSmpNFdiVnjLTrZbw9Y9q89Dz0ARchRu1MbBtRvANxEFN0Hh9N305lEsWaW0VWy'
client = Client(api_key, api_secret)
# print(api_key, api_secret)

# client.API_URL = 'https://testnet.binance.vision/api'
# # get balances for all assets & some account information
# print(client.get_account())
# # get balance for a specific asset only (BTC)
# print(client.get_asset_balance(asset='BTC'))

max = 0
min = 0
max_time = ""

def telegram_bot_sendtext(bot_message):
    
    bot_token = ''
    bot_chatID = ''
    send_text = 'https://api.telegram.org/bot' + '1984695297:AAEX20AH_trDS9TT4ljpDR22X2J5P2Kh73U' + '/sendMessage?chat_id=' + '2056522270' + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

def get_min_court(my_symbol):
    global max
    global min
    global max_time
    
    while 1:
        # get latest price from Binance API
        btc_price = client.get_symbol_ticker(symbol=my_symbol)
       
        # Calcul of current position
        if (max < float(btc_price["price"])):
            max = float(btc_price["price"])
            max_time = str(datetime.datetime.now())
        if (min > float(btc_price["price"])):
            min = float(btc_price["price"])
        var = (max / float(btc_price["price"]))
        if( var > 1.05):
            # print("Sell! -> variation is  "+ str(max / float(btc_price["price"])))
            telegram_bot_sendtext("Sell! -> variation is  "+ str(max / float(btc_price["price"])))

        # Print current value
        print(str(datetime.datetime.now())+ "    |   " + btc_price["price"] + "    |   " + str(max) + "    |   " + max_time + "    |   " + str(var))

        # WAit 5sec
        time.sleep(5)


if __name__ == "__main__":
   get_min_court("BTCEUR")
