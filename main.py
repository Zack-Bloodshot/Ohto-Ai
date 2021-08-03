from pyrogram import Client as Bot
from pyrogram import idle
import logging 
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID, SESSION_NAME
from Summon.summon import temo
import time 

bot = Bot(
    ":memory:",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="handlers")
)

client = Bot(SESSION_NAME, API_ID, API_HASH)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)
logger = logging.getLogger('__name__') 


print("Ohto Ai: Starting.....!!!")

client.start()
bot.start()
#idle()
#bot.stop()

#bot.send_message(int(OWNER_ID), "Im onlime")