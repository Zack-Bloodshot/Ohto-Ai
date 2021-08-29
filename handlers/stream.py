from pyrogram import Client, filters
from pyrogram.types import Message, Voice
from youtube_search import YoutubeSearch 
from callsmusic import mp, quu, block_chat
import callsmusic
import converter
from pyrogram.errors import PeerIdInvalid, ChannelInvalid
from pyrogram.errors import exceptions
from downloaders import youtube
from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)
from config import BOT_NAME as bn, DURATION_LIMIT
from helpers.filters import command, other_filters
from helpers.decorators import errors
from helpers.decorators import authorized_users_only
from helpers.decorators import authorized_users_only2
from config import API_ID, API_HASH, BOT_TOKEN, PLAY_PIC, BOT_USERNAME, OWNER_ID, UBOT_ID

@Client.on_message(filters.command(["stream", f"stream@{BOT_USERNAME}"]) & other_filters)
@errors
@authorized_users_only
async def stream_vid(client: Client, message: Message):
  video = message.reply_to_message.video if message.reply_to_message else None
  if not video:
    return await message.reply_text('Reply to a video...')
  dl = await message.reply_to_message.download()
  try:
      group_call = await mp.call(message.chat.id)
  except RuntimeError:
      return await message.reply_text('The vc seems to be off.....')
  except ChannelInvalid:
      return await message.reply_text('Seems like my assistant is not in the chat!')
  except Exception as e:
      return await message.reply_text(f'{type(e).__name__}: {e}')
  await group_call.set_video_capture(dl)
  block_chat.append(message.chat.id)