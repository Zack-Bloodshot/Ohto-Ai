from pyrogram import Client, filters
from pyrogram.types import Message, Voice
from youtube_search import YoutubeSearch 
from callsmusic import mp, quu, block_chat, FFMPEG_PRO
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
import asyncio
import os
import ffmpeg

@Client.on_message(filters.command(["stream", f"stream@{BOT_USERNAME}"]) & other_filters)
async def stream(client: Client, message: Message):
  if message.chat.id in block_chat:
    m = await message.reply_text('Please stop present stream to start new....')
    await asyncio.sleep(3)
    return await m.delete()
  video = (message.reply_to_message.video or message.reply_to_message.document) if message.reply_to_message else None
  if not video:
    return await message.reply_text('Reply to a file or a video....')
  if not (video.file_name.endswith('.mkv') or video.file_name.endswith('.mp4')):
    return await message.reply_text('Not a valid format...')
  m = await message.reply_text('Downloading....will take time depending on video size...')
  file_name = f'{video.file_unique_id}.{video.file_name.split(".", 1)[-1]}'
  dl = await message.reply_to_message.download(file_name)
  await m.edit('Joining....')
  group_call = await mp.stream(message.chat.id)
  await group_call.start_video(dl)
  await m.delete()
  await message.reply_text(f'Streaming {video.file_name}...')
  block_chat.append(message.chat.id)
  
@Client.on_message(filters.command(["loopstream", f"loopstream@{BOT_USERNAME}"]) & other_filters)
async def stream_loop(client: Client, message: Message):
  if message.chat.id in block_chat:
    m = await message.reply_text('Please stop present stream to start new....')
    asyncio.sleep(3)
    return await m.delete()
  video = (message.reply_to_message.video or message.reply_to_message.document) if message.reply_to_message else None
  if not video:
    return await message.reply_text('Reply to a file or a video....')
  if not (video.file_name.endswith('.mkv') or video.file_name.endswith('.mp4')):
    return await message.reply_text('Not a valid format...')
  m = await message.reply_text('Downloading....will take time depending on video size...')
  file_name = f'{video.file_unique_id}.{video.file_name.split(".", 1)[-1]}'
  dl = await message.reply_to_message.download(file_name)
  
  await m.delete()
  await message.reply_text(f'On loop!')
  
@Client.on_message(filters.command(["livestream", f"livestream@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only
async def stream_live(client: Client, message: Message):
  if message.chat.id in block_chat:
    m = await message.reply_text('Please stop present stream to start new....')
    asyncio.sleep(3)
    return await m.delete()
  try:
    video = message.text.split(' ', 1)[1]
  except IndexError:
    return await message.reply_text('provide url..in message..')
  try:
      group_call = await mp.call(message.chat.id)
  except RuntimeError:
      return await message.reply_text('The vc seems to be off.....')
  except ChannelInvalid:
      return await message.reply_text('Seems like my assistant is not in the chat!')
  except Exception as e:
      return await message.reply_text(f'{type(e).__name__}: {e}')
  input_filename = f'streamat{message.chat.id}'
  os.mkfifo(input_filename)
  group_call.input_filename = input_filename
  process = ffmpeg.input(video).output(
    input_filename,
    format="s16le",
    acodec="pcm_s16le",
    ac=2,
    ar="48k",
    loglevel="error",
  ).overwrite_output().run_async()
  await group_call.set_video_capture(video)
  FFMPEG_PRO[message.chat.id] = process
  block_chat.append(message.chat.id)
  await message.reply_text(f'Cross fingers and check vc!')
  