from pyrogram import Client as Bot
import logging 
from callsmusic import run
from config import API_ID, API_HASH, BOT_TOKEN
from Summon.summon import temo
import time 

bot = Bot(
    ":memory:",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="handlers")
)

Start_Time = time.time()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)
 
bot.start()
run()
