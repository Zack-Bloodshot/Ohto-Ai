from pyrogram import Client as Bot
import logging 
from callsmusic import run
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID
from Summon.summon import temo
import time 

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
run()

bot.send_message(int(OWNER_ID), "Im onlime")