# import telegram
# test = telegram.Bot(token='2053306894:AAGAHjOmNiXLFCsUkdxTW2M6dJMfX6UQO2c')
# me = test.get_me()
# print(f"🤖 Hello, I'm {me.first_name}.\nHave a nice Day!")
# test.close()

# from telegram.ext import Updater
# updater = Updater('2053306894:AAGAHjOmNiXLFCsUkdxTW2M6dJMfX6UQO2c', use_context=True)

# import asyncio
# from aiogram import Bot

# BOT_TOKEN = ""

# async def main():
#     bot = Bot(token='2053306894:AAGAHjOmNiXLFCsUkdxTW2M6dJMfX6UQO2c')

#     try:
#         me = await bot.get_me()
#         print(f"🤖 Hello, I'm {me.first_name}.\nHave a nice Day!")
#     finally:
#         await bot.close()

# asyncio.run(main())

import requests

def telegram_bot_sendtext(bot_message):
    
    bot_token = ''
    bot_chatID = ''
    send_text = 'https://api.telegram.org/bot' + '2053306894:AAGAHjOmNiXLFCsUkdxTW2M6dJMfX6UQO2c' + '/sendMessage?chat_id=' + '2056522270' + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()
    

test = telegram_bot_sendtext("Testing Telegram bot")
print(test)