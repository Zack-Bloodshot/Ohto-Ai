from os import path

from pyrogram import Client, filters
from pyrogram.types import Message, Voice
from youtube_search import YoutubeSearch 
from callsmusic.queues.queues import qget
import callsmusic
import converter
from pyrogram.errors import PeerIdInvalid
from downloaders import youtube
from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)
from config import BOT_NAME as bn, DURATION_LIMIT
from helpers.filters import command, other_filters
from helpers.decorators import errors
from helpers.decorators import authorized_users_only
from helpers.errors import DurationLimitError
from helpers.gets import get_url, get_file_name
from config import API_ID, API_HASH, BOT_TOKEN
quu = {} 

@Client.on_message(filters.group & filters.new_chat_members)
@errors
async def selfwelc(client: Client, message: Message):
  for user in message.new_chat_members:
    if user.id == 1704447681:
      await message.reply_text("Yayy, a new adventure, cant wait to share with Abhi-sama!!")
      chat_name = message.chat.title
      get = await client.get_chat(message.chat.id)
      if get.username:
        l = "https://t.me/" + get.username
      else:
        l = " "
      await client.send_message(chat_id = 1285226731, text = f"#NEW_GROUP\n**Title: {chat_name}\n[...](l)**", parse_mode ="md")

@Client.on_message(filters.command(["queue", "queue@OhtoAiPlaysBot"]) & other_filters)
@errors
@authorized_users_only
async def que(client: Client, message: Message):
  global quu
  try:
    why = quu[message.chat.id]
  except KeyError:
    why = []
  print(why)
  titt = message.chat.title 
  tex = f"**Songs in {titt}...\n\n"
  count = 0
  if len(why) >= 1:
    for i in why:
      tex +=  "•" 
      tex += i 
      if i == why[0]:
        tex += "**`(playin now)`**"
      tex += "\n\n"
      count += 1
    print(tex)
  else:
    tex = "**No songs in queue right now!"
  tex += "**"
  print(tex) 
  markup = InlineKeyboardMarkup([[InlineKeyboardButton(text = "Check Private!", url = "https://t.me/OhtoAiPlaysBot")]])
  m = await message.reply_text("Its in your pm!, if u contacted with me before!!", reply_markup = markup) 
  try:
    await client.send_message(chat_id = message.from_user.id, text = tex)
  except PeerIdInvalid:
    await m.delete()
    await message.reply_text("Please go and contact me in pm kek!", reply_markup = markup)

@Client.on_message(filters.command(["start", "start@OhtoAiPlaysBot"]) & other_filters)
@errors
async def startgrp(_, message: Message):
  await message.reply_text("Im awake and runnin' perfectly!!")
  
@Client.on_message(filters.command(["help", "help@OhtoAiPlaysBot"]) & other_filters)
@errors
async def helpgrp(_, message: Message):
  markup = InlineKeyboardMarkup([[InlineKeyboardButton(text = "Help", url = "t.me/OhtoAiPlaysBot?start=help")]])
  await message.reply_text("Yess!!, get to know me in my pm!", reply_markup = markup)

@Client.on_message(filters.command(["play", "play@OhtoAiPlaysBot"]) & other_filters)
@errors
@authorized_users_only
async def play(_, message: Message):
    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
    url = get_url(message)
    me = message.text.split(None, 1)
    if len(me) >= 2:
      args = me[1]
    else:
      args = "None"
    ruuta = " "
    text = " "
    markup = " "
    m = await message.reply_text("Wait-a-min....(^_-)")
    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"Videos longer than {DURATION_LIMIT} minute(s) aren't allowed!\n🤐 The provided video is {audio.duration / 60} minute(s)"
            )

        file_name = get_file_name(audio)
        text += "**Playin[...](https://telegra.ph/file/49fd302f1c0738257728c.mp4)**"
        markup = InlineKeyboardMarkup([[InlineKeyboardButton(text = "🦄", callback_data = "na")]])
        await m.edit("Processing...")
        ruuta += "Tg file..., name unknown"
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name)) else file_name
        )
    elif url:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(url, max_results=1).to_dict()
            count += 1
        markup = InlineKeyboardMarkup([[InlineKeyboardButton(text = "Go To Video", url = url)]])
        title = results[0]["title"]
        thumb =results[0]["thumbnails"][0]
        await m.edit("Processing...just-a-sec...")
        try:
          thumb.pop() 
          tum = " ".join(thumb)
        except AttributeError:
          tum = thumb 
        text += f"\n**{title}[..]({tum})**"
        ruuta += title
        duration = results[0]["duration"]
        text += f"\n**Duration: {str(duration)}**"
        channel = results[0]["channel"]
        text += f"\n**Artist: {channel}**"
        file_path = await converter.convert(youtube.download(url))
    elif not args == "None":
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(args, max_results=1).to_dict()
            count += 1
        vidId = results[0]['id']
        link = "https://youtu.be/" + vidId
        await m.edit("Downloading...")
        file_path = await converter.convert(youtube.download(link))
        markup = InlineKeyboardMarkup([[(InlineKeyboardButton(text = "Go to video", url = link))]]) 
        title = results[0]["title"]
        thumb =results[0]["thumbnails"][0]
        try:
          thumb.pop()
          tum = " ".join(thumb)
        except AttributeError:
          tum = thumb
        text += f"\n**{title}[..]({tum})**"
        ruuta += title 
        duration = results[0]["duration"]
        text += f"\n**Duration: {str(duration)}**"
        await m.edit("Processing...just-a-sec..")
        channel = results[0]["channel"]
        text += f"\n**Artist: {channel}**"
    else:
      await m.delete()
      markup = InlineKeyboardMarkup([[(InlineKeyboardButton("Search And Play ", switch_inline_query_current_chat = ""))]])
      await message.reply_text(f"You did not give me anything to play!", reply_markup = markup)
      return 

    if message.chat.id in callsmusic.pytgcalls.active_calls:
        global quu
        quu[message.chat.id].append(ruuta)
        text += f"**\nQueued at position #{await callsmusic.queues.put(message.chat.id, file_path=file_path)} !**"
        await m.delete()
        await message.reply_text(text, parse_mode = "md", reply_markup = markup) 
    else:
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        await m.delete()
        quu[message.chat.id] = [ruuta]
        await message.reply_text(text, reply_markup = markup, parse_mode = "md")
