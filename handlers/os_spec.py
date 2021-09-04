from pyrogram import Client, filters
from pyrogram.types import Message
import config
import subprocess
from helpers.filters import command, other_filters

@Client.on_message(filters.command(["neofetch", f"neofetch@{config.BOT_USERNAME}"]) & other_filters)
async def neo_fetcher(_, message: Message):
  if message.from_user.id != config.OWNER_ID:
    return 
  process = subprocess.Popen(
                'neofetch',
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
  out = process.stdout.read()[:-1].decode("utf-8")
  f = open('neofetch.txt', 'w')
  f.write(out)
  f.close()
  await message.reply_document(document='neofetch.txt')