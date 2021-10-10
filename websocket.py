import os
import time

from binance import ThreadedWebsocketManager

api_key       = os.environ.get('binance_api')
api_secret    = os.environ.get('binance_secret')

def main():

    symbol = 'BTCUSDT'

    twm = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)
    # start is required to initialise its internal loop
    twm.start()

    def handle_socket_message(msg):
        print(f"message type: {msg['e']}")
        print(msg['c'])

    # twm.start_kline_socket(callback=handle_socket_message, symbol=symbol)
    ts = twm.trade_socket('BTCUSDT')
    twm.join()


if __name__ == "__main__":
   main()