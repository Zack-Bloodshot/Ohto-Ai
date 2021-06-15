from os import getenv
import time 
from dotenv import load_dotenv

load_dotenv()

START_TIME = time.time()

SESSION_NAME = getenv("SESSION_NAME", "session")

BOT_TOKEN = getenv("BOT_TOKEN")

BOT_NAME = getenv("BOT_NAME")

OWNER_ID = int(getenv("OWNER_ID")) 

UBOT_ID = int(getenv("BOT_ID"))

START_PIC = getenv("START_PIC")

PLAY_PIC = getenv("PLAY_PIC")

API_ID = int(getenv("API_ID"))

API_HASH = getenv("API_HASH")

BOT_USERNAME = getenv("BOT_USERNAME")

DURATION_LIMIT = int(getenv("DURATION_LIMIT", "7"))

COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ !").split())

SUDO_USERS = list(map(int, getenv("SUDO_USERS").split()))
