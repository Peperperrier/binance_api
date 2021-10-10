#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import os
import binance
import time
import datetime
import requests
import threading

from binance.client import Client

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# init
api_key     = os.environ.get('binance_api')
api_secret  = os.environ.get('binance_secret')
client      = Client(api_key, api_secret)

# Value to check crypto court
max = 0
min = 0
max_time = ""
str_btc_price = ""
var = 0

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def telegram_bot_sendtext(bot_message):
    
    bot_token = ''
    bot_chatID = ''
    send_text = 'https://api.telegram.org/bot' + '2053306894:AAGAHjOmNiXLFCsUkdxTW2M6dJMfX6UQO2c' + '/sendMessage?chat_id=' + '2056522270' + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

def get_min_court():
    global max
    global min
    global max_time
    global str_btc_price
    global var

    old_time = 80

    while 1:
        # get latest price from Binance API
        btc_price = client.get_symbol_ticker(symbol="BTCUSDT")
        str_btc_price = str(float(btc_price["price"]))

        # Calcul of current position
        if (max < float(btc_price["price"])):
            max = float(btc_price["price"])
            max_time = str(datetime.datetime.now())
        if (min > float(btc_price["price"])):
            min = float(btc_price["price"])
        var = (max / float(btc_price["price"]))
        
        if((old_time != datetime.datetime.now().minute and var > 1.05)):
            # print("Sell! -> variation is  "+ str(max / float(btc_price["price"])))
            old_time = datetime.datetime.now().minute
            telegram_bot_sendtext("Sell! -> variation is  "+ str(max / float(btc_price["price"])))

        # Print current value
        print(str(datetime.datetime.now())+ "    |   " + btc_price["price"] + "    |   " + str(max) + "    |   " + max_time + "    |   " + str(var))

        # WAit 5sec
        time.sleep(5)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def x_isalive(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    global x
    update.message.reply_text(x.isAlive())

def max_command(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(str(datetime.datetime.now())+ "    |   " + str_btc_price + "    |   " + str(max) + "    |   " + max_time + "    |   " + str(var))
    # update.message.reply_text("price" + str_btc_price)

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater('2053306894:AAGAHjOmNiXLFCsUkdxTW2M6dJMfX6UQO2c')

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("max", max_command))
    dispatcher.add_handler(CommandHandler("live", x_isalive))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    x = threading.Thread(target=get_min_court)
    x.start()
    main()