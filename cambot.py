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
import time
import datetime
import requests
import threading
import configparser

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def telegram_bot_sendtext(bot_message):
    
    bot_token = ''
    bot_chatID = ''
    send_text = 'https://api.telegram.org/bot' + '1984695297:AAEX20AH_trDS9TT4ljpDR22X2J5P2Kh73U' + '/sendMessage?chat_id=' + '2056522270' + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

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

def start_motion(update: Update, context: CallbackContext) -> None:
    """Send an OS command to start services."""
    update.message.reply_text("Trying to start motion")
    os.system("sudo systemctl start motion" )

def stop_motion(update: Update, context: CallbackContext) -> None:
    """Send an OS command to start services."""
    update.message.reply_text("Trying to stop motion")
    os.system("sudo systemctl stop motion" )

def last(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    for file in os.listdir("./"):
        if file.endswith(".mkv"):
            my_file = file
    # print(my_file)
    update.message.reply_text(str(my_file))
    update.message.reply_video(video=open(os.path.join('/tmp/motion/', my_file), 'rb'))
    
def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater('1984695297:AAEX20AH_trDS9TT4ljpDR22X2J5P2Kh73U')

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("last", last))
    dispatcher.add_handler(CommandHandler("motion", start_motion))
    dispatcher.add_handler(CommandHandler("stop", stop_motion))

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
    main()