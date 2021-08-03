from pyrogram import Client as Bot
from pyrogram import idle
import logging
import config
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID, SESSION_NAME
from Summon.summon import temo
import time 

client = Bot(config.SESSION_NAME, config.API_ID, config.API_HASH)

bot = Bot(
    ":memory:",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="handlers")
)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)
logger = logging.getLogger('__name__') 


print("Ohto Ai: Starting.....!!!")

bot.start()
client.run()
#idle()
#bot.stop()

#bot.send_message(int(OWNER_ID), "Im onlime")