from os import path
from sql import calls as sql
from sql import auth as sql2
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
from helpers.errors import DurationLimitError
from helpers.gets import get_url, get_file_name
from config import API_ID, API_HASH, BOT_TOKEN, PLAY_PIC, BOT_USERNAME, OWNER_ID, UBOT_ID
import time 
import config
from config import START_TIME as st

quu = quu

sleep_time = 3

@Client.on_message(filters.group & filters.new_chat_members)
@errors
async def selfwelc(client: Client, message: Message):
  for user in message.new_chat_members:
    if user.id == int(UBOT_ID):
      if config.SUMMONER == 'False':
        await message.reply_text("Demmm kek, a new adventure, can't wait to tell Abhi-sama")
      else:
        await message. reply_text("Ahk sorry, imma private bot! Deploy one!")
      chat_name = message.chat.title
      get = await client.get_chat(message.chat.id)
      if get.username:
        l = "https://t.me/" + get.username
      else:
        l = " "
      await client.send_message(chat_id = OWNER_ID, text = f"#NEW_GROUP\n**Title: {chat_name}\n[...](l)**", parse_mode ="md")

@Client.on_message(filters.command(["queue", f"queue@{BOT_USERNAME}"]) & other_filters)
@errors
@authorized_users_only2
async def que(client: Client, message: Message):
  try:
    await message.delete()
  except Exception as e:
    print(e)
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
      tex +=  str(count)
      tex += i 
      if i == why[0]:
        tex += "`(playin now)`"
      tex += "\n\n"
      count += 1
    print(tex)
  else:
    tex = "**No songs in queue right now!"
  tex += "**"
  print(tex) 
  markup = InlineKeyboardMarkup([[InlineKeyboardButton(text = "Check Private!", url = f"https://t.me/{BOT_USERNAME}")]])
  m = await message.reply_text("Its in your pm!, if u contacted with me before!!", reply_markup = markup) 
  try:
    await client.send_message(chat_id = message.from_user.id, text = tex)
  except PeerIdInvalid:
    await m.delete()
    m = await message.reply_text("Please go and contact me in pm kek!", reply_markup = markup)
  time.sleep(sleep_time)
  await m.delete()

def send_now_playing(chat_id):
  if queues.is_empty(chat_id):
   return
  np = quu[chat_id][0]
  tex = f"Stream Changed!\nNow playing:\n\n **{np}**"
  m = Client.send_message(chat_id, tex)

def grt(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time



@Client.on_message(filters.command(["now", f"now@{BOT_USERNAME}"]) & other_filters)
@errors
async def showplay(_, message: Message):
  global quu
  if not sql.is_call(message.chat.id):
    return await message.reply("Nuthin playin...")
  song = quu[message.chat.id][0]
  if message.reply_to_message:
    m = await message.reply_to_message.reply(f"**Now playin in {message.chat.title}\n\n{song}**")
  else:
    m = await message.reply(f"**Now playing in {message.chat.title}\n\n{song}**")
  try:
    await message.delete()
  except Exception:
    pass
  time.sleep(5)
  await m.delete()
  
@Client.on_message(filters.command(["start", f"start@{BOT_USERNAME}"]) & other_filters)
@errors
async def startgrp(_, message: Message):
  starto = grt(time.time() - st)
  await message.reply_text(f"Im awake and runnin' perfectly!!\nHaven't napped since: `{starto}`")
  
@Client.on_message(filters.command(["help", f"help@{BOT_USERNAME}"]) & other_filters)
@errors
async def helpgrp(_, message: Message):
  markup = InlineKeyboardMarkup([[InlineKeyboardButton(text = "Help", url = f"t.me/{BOT_USERNAME}?start=help")]])
  await message.reply_text("Yess!!, get to know me in my pm!", reply_markup = markup)

def erro(mid, fp, ru):
  sql.set_off(mid)
  global quu
  try: 
    callsmusic.pytgcalls.join_group_call(mid, fp)
  except Exception:
    return False
  sql.set_on(mid)
  quu[mid] = [ru]
  return True
 

@Client.on_message(filters.command(["play", f"play@{BOT_USERNAME}"]) & other_filters)
@errors
@authorized_users_only2
async def play(_, message: Message):
    if message.chat.id in block_chat:
      return await message.reply('Seems like there is a video stream going on...')
    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
    try:
      group_call = await mp.call(message.chat.id)
    except RuntimeError:
        return await message.reply_text('The vc seems to be off.....')
    except ChannelInvalid:
        return await message.reply_text('Seems like my assistant is not in the chat!')
    except Exception as e:
        return await message.reply_text(f'{type(e).__name__}: {e}')
    req_name = f"Requested By: {message.from_user.first_name}\n"
    req_user = f"Requested By: [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n"
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
    try:
      await message.delete()
    except Exception:
      pass
    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
          raise DurationLimitError(f"Videos longer than {DURATION_LIMIT} minute(s) aren't allowed!\n🤐 The provided video is {audio.duration / 60} minute(s)")

        file_name = get_file_name(audio)
        title = f"{audio.file_name}"[:-4]
        text += f"**{title}[...]({PLAY_PIC})\n"
        text += f"{req_user}**"
        markup = InlineKeyboardMarkup([[InlineKeyboardButton(text = "🦄", callback_data = "na")]])
        await m.edit("Processing...")
        ruuta += f"{title}\n{req_name}"
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
        duration = results[0]["duration"]
        text += f"\n**Duration: {str(duration)}**"
        #channel = results[0]["channel"]
        # += f"\n**Artist: {channel}**"
        text += f"\n**{req_user}**"
        file_path = await converter.convert(youtube.download(url))
        ruuta += f"{title}\nDuration: {duration}\n{req_name}"
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
        duration = results[0]["duration"]
        text += f"\n**Duration: {str(duration)}**"
        await m.edit("Processing...just-a-sec..")
        #channel = results[0]["channel"]
        #text += f"\n**Artist: {channel}**"
        text += f"\n**{req_user}**"
        ruuta += f"{title}\nDuration: {duration}\n{req_name}"
    else:
      await m.delete()
      markup = InlineKeyboardMarkup([[(InlineKeyboardButton("Search And Play ", switch_inline_query_current_chat = ""))]])
      await message.reply_text(f"You did not give me anything to play!", reply_markup = markup)
      return 

    if sql.is_call(message.chat.id):
        global quu
        try:
          quu[message.chat.id].append(ruuta)
        except Exception:
          sql.set_off(message.chat.id)
          await message.reply_text('Ahk! sorry, try again!')
        text += f"**\nQueued at position #{await callsmusic.queues.put(message.chat.id, file_path=file_path)} !**"
        await m.delete()
        m = await message.reply_text(text, parse_mode = "md", reply_markup = markup) 
        time.sleep(sleep_time)
        await m.delete() 
    else:
        try: 
          group_call.input_filename = file_path
        except Exception as e:
          print(e)
          await m.delete()
          await message.reply(e)
          return 
        sql.set_on(message.chat.id)
        await m.delete()
        quu[message.chat.id] = [ruuta]
        m = await message.reply_text(text, reply_markup = markup, parse_mode = "md")
        time.sleep(sleep_time)
        await m.delete()

