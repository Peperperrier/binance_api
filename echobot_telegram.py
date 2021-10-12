#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
import configparser

from binance.client import Client

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# init
api_key         = os.environ.get('binance_api')
api_secret      = os.environ.get('binance_secret')
client          = Client(api_key, api_secret)
TOKEN           = '2001873085:AAGwq7zXUZqq15-0Rvcp7hAooFHVquwoNHQ'
CHAT_ID         = '2056522270'


# Value to check crypto court
config = configparser.ConfigParser()
config.read('config.ini')
max = float(config['BINANCE']['max_value'])
str_max_time = str(config['BINANCE']['max_time'])
min = float(config['BINANCE']['min_value'])
str_min_time = str(config['BINANCE']['min_time'])

trigger = float(config['BINANCE']['trigger'])
trig_max = float(config['BINANCE']['trig_max'])
trig_min = str(config['BINANCE']['trig_min'])

en_min = False
en_max = False

str_btc_price = ""
btc_buy_price = 0
var_max = 0
var_min = 0



# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

def telegram_bot_sendtext(bot_message):
    
    bot_token = ''
    bot_chatID = ''
    send_text = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' + CHAT_ID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

def get_min_court():
    global max
    global min
    global str_max_time
    global str_min_time

    global str_btc_price
    global var_max
    global var_min
    global en_max
    global en_min
    global btc_buy_price

    global trigger
    global trig_max
    global trig_min

    old_time = 80

    while 1:
        # get latest price from Binance API
        btc_price = client.get_symbol_ticker(symbol="BTCEUR")
        str_btc_price = str(float(btc_price["price"]))

        # Calcul of current position
        if (max < float(btc_price["price"])):
            max = float(btc_price["price"])
            config['BINANCE']['max_value'] = str(max)
            str_max_time = str(datetime.datetime.now())
            config['BINANCE']['max_time'] = str_max_time
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            
        if (min > float(btc_price["price"])):
            min = float(btc_price["price"])
            config['BINANCE']['min_value'] = str(min)
            str_min_time = str(datetime.datetime.now())
            config['BINANCE']['min_time'] = str_min_time
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
        
        # Calcul de variation    
        var_max = (max / float(btc_price["price"]))
        var_min = (float(btc_price["price"]) / min)
        
        if (old_time != datetime.datetime.now().minute):
            old_time = datetime.datetime.now().minute
            if ((en_max == True) and var_max > trigger):
                telegram_bot_sendtext("Sell! -> variation is  "+ str(max / float(btc_price["price"])))

            if ((en_min == True) and var_min > trigger):
                telegram_bot_sendtext("Buy! -> variation is  "+ str(float(btc_price["price"]) / min))

        # Print current value
        # print(str(datetime.datetime.now())+ "    |   " + btc_price["price"] + "    |   " + str(max) + "    |   " + max_time + "    |   " + str(var))

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
    
def max_command(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(str(datetime.datetime.now())+ "    |   " + str_btc_price + "    |   " + str(max) + "    |   " + str_max_time + "    |   " + str(var_max))
    # update.message.reply_text("price" + str_btc_price)

def min_command(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(str(datetime.datetime.now())+ "    |   " + str_btc_price + "    |   " + str(min) + "    |   " + str_min_time + "    |   " + str(var_min))
    # update.message.reply_text("price" + str_btc_price)

def en_max_command(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    global en_max
    en_max = True
    update.message.reply_text("en_max = True")

def en_min_command(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    global en_min
    en_min = True
    update.message.reply_text("en_min = True")

def dis_max_command(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    global en_max
    en_max = False
    update.message.reply_text("en_max = False")

def dis_min_command(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    global en_min
    en_min = False
    update.message.reply_text("en_min = False")

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("max", max_command))
    dispatcher.add_handler(CommandHandler("min", min_command))
    dispatcher.add_handler(CommandHandler("enablemax", en_max_command))
    dispatcher.add_handler(CommandHandler("enablemin", en_min_command))
    dispatcher.add_handler(CommandHandler("disablemax", dis_max_command))
    dispatcher.add_handler(CommandHandler("disablemin", dis_min_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    telegram_bot_sendtext("Bot is started ! ")
    x = threading.Thread(target=get_min_court)
    x.start()
    main()
