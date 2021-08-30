from asyncio.queues import QueueEmpty
from datetime import datetime as kek
from sql import calls as sql
from pyrogram import Client, filters 
from pyrogram.types import Message, Chat, User
import callsmusic
from callsmusic import mp, quu, block_chat
from callsmusic import client as player
from pyrogram.errors import PeerIdInvalid
from pyrogram.errors import exceptions as pexc
from sql import auth as ats
from config import BOT_NAME as BN
from config import SUDO_USERS
from helpers.filters import command, other_filters
from helpers.decorators import errors, authorized_users_only, authorized_users_only2
from config import BOT_USERNAME
from config import PLAY_PIC, SUMMONER
from config import UBOT_ID as ubot

def mention(name, userid):
  return f"[{name}](tg://user?id={userid})"

@Client.on_message(filters.command(["summon", f"summon@{BOT_USERNAME}"]))
@authorized_users_only2
async def summon(client: Client, message: Message): 
  if not SUMMONER == 'False':
    await message.reply_text('Sorry, this is a private music bot!')
    return
  m = await message.reply_text("Yea well, waitto, will take some time!")
  try:
    hek = message.chat.username
    if  hek == None:
      hek = await client.export_chat_invite_link(message.chat.id)
  except BaseException:
    return await message.reply_text('Ahk! Looks like im not admin and the chat is private!')
  try:
    await player.join_chat(hek)
  except pexc.bad_request_400.UserAlreadyParticipant:
    return await m.edit('Userbot is here!')
  await m.edit("Summon Successfull! Now enjoy playing!")

@Client.on_message(filters.command(["ping", f"ping@{BOT_USERNAME}"]))
async def pong(_, message: Message):
  start = kek.now()
  m = await message.reply("**PONG!**")
  end = kek.now()
  pon = (end - start).microseconds / 1000
  await m.edit(f"**PONG!\nPing Time: `{pon}`")

@Client.on_message(filters.command(["reset", f"reset@{BOT_USERNAME}"]) & other_filters)
@errors 
@authorized_users_only2
async def res(_, message: Message): 
  global quu
  try:
    callsmusic.queues.clear(message.chat.id)
  except QueueEmpty:
    await message.reply("Queue empty")
  if sql.is_call(message.chat.id):
    sql.set_off(message.chat.id)
  quu[message.chat.id] = []
  try: 
    await mp.leave(message.chat.id)
  except Exception:
    pass
  try:
    block_chat.pop(message.chat.id)
  except Exception:
    pass
  await message.reply("**Reset successful..!!!**")

@Client.on_message(filters.command(["auth", f"auth@{BOT_USERNAME}"]) & other_filters)
@errors 
@authorized_users_only 
async def aut(_, message: Message):
  re = message.reply_to_message
  if not re: 
    return await message.reply("Reply to a user... to authorize...")
  reply = re.from_user
  if ats.is_approved(message.chat.id, reply.id):
    return await message.reply(f"**[{reply.first_name}](tg://user?id={reply.id}) is already authorizedd in {message.chat.title}**")
  else: 
    ats.approve(message.chat.id, reply.id)
    return await message.reply(f"[{reply.first_name}](tg://user?id={reply.id}) was authorized in {message.chat.title}")

async def meme_get(chat: Chat, user): 
  return await chat.get_member(user)

@Client.on_message(filters.command(["remauth", f"remauth@{BOT_USERNAME}"]) & other_filters)
@errors 
@authorized_users_only 
async def remauth(_, message: Message): 
  reply = message.reply_to_message
  if not reply: 
    user = message.text[8:] 
    if user == '':
      return await message.reply("Reply To a user or use the user id to unauthorize.. ")
  else:
    user = reply.from_user.id
  if ats.is_approved(message.chat.id, user):
    ats.disapprove(message.chat.id, user)
    try:
      meme = await meme_get(message.chat, int(user))
    except PeerIdInvalid:
      meme = False
    text = "{} was unauthorized in {}"
    if not meme == False:
      kek = mention(meme.user['first_name'], user)
      text = text.format(kek, message.chat.title)
      await message.reply(text) 
    else:
      hek = f"`{user}` (I hadn't met this user in pm)"
      text= text.format(hek, message.chat.title)
      await message.reply(text)
  else: 
    return await message.reply("This user is already not authorized..")



@Client.on_message(filters.command(["listauth", f"listauth@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only 
async def listauth(chat: Chat, message: Message):
    chat_title = message.chat.title
    msg = "The following users are authorized...\n"
    approved_users = ats.list_approved(message.chat.id)
    count = 0
    for i in approved_users:
      try: 
        member = await meme_get(message.chat, int(i.user_id))
      except PeerIdInvalid: 
        member = " "
      count += 1
      if not member == " ": 
        msg += f"{count}) `{i.user_id}`: {member.user['first_name']}\n"
      else:
        msg += f"{count}) `{i.user_id}`: (I didn't see him yet in pm )\n"
    if msg.endswith("approved.\n"):
        message.reply(f"No users are approved in {chat_title}.")
        return ""
    else:
      await message.reply(msg)

@Client.on_message(filters.command(["pause", f"pause@{BOT_USERNAME}"]) & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    if not sql.is_call(message.chat.id):
      return await message.reply("Nuthin playin.... ")
    group_call = await mp.call(message.chat.id)
    try:
      group_call.pause_playout()
      await message.reply_text('Paused! hek!')
    except Exception:
      await message.reply_text('Could not!!')

@Client.on_message(filters.command(["resume", f"resume@{BOT_USERNAME}"]) & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    if not sql.is_call(message.chat.id):
      return await message.reply("Nuthin playin...")
    group_call = await mp.call(message.chat.id)
    try:
      group_call.resume_playout()
      await message.reply_text('Resumed!')
    except Exception:
      await message.reply_text('Could Not!')


@Client.on_message(filters.command(["stop", f"stop@{BOT_USERNAME}"]) & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    if message.chat.id in block_chat:
      await mp.leave(message.chat.id)
      block_chat.pop(message.chat.id)
      return await message.reply_text('Stopped streaming....')
    if not sql.is_call(message.chat.id):
        await message.reply_text("Nuthin Streamin'....... ig so.. ", parse_mode = "md")
    else:
        try: 
          callsmusic.queues.clear(message.chat.id)
        except QueueEmpty: 
          pass 
        quu[message.chat.id] = []
        await mp.leave(message.chat.id)
        sql.set_off(message.chat.id)
        await message.reply_text(f"Ahh, its peaceful now, Byee[...]({PLAY_PIC})", parse_mode = "md")


@Client.on_message(filters.command(["skip", f"skip@{BOT_USERNAME}"]) & other_filters)
@errors
@authorized_users_only2
async def skip(_, message: Message):
    if message.chat.id in block_chat:
      return await message.reply_text('Cant skip video stream...')
    if not sql.is_call(message.chat.id):
      return await message.reply("Baka nothing to skip..!")
    if callsmusic.queues.is_empty(message.chat.id):
      try:
        await mp.leave(message.chat.id)
        sql.set_off(message.chat.id)
      except Exception:
        pass
      await message.reply_text("Ahh baka, Nuthin to skip..... ",parse_mode = "md")
    else:
        callsmusic.queues.task_done(message.chat.id)
        try:
          why = quu[message.chat.id]
        except KeyError:
          why = []
        try: 
          why.pop(0)
        except IndexError: 
          pass
        if callsmusic.queues.is_empty(message.chat.id):
            nex_song = " "
            await mp.leave(message.chat.id)
            sql.set_off(message.chat.id)
        else:
            try:
              nex_song = "**Now playin: " + why[0] + "**"
            except IndexError:
              nex_song = " "
            gp = await mp.call(message.chat.id)
            gp.input_filename = callsmusic.queues.get(message.chat.id)["file_path"]
        await message.reply_text(f"Skipped....!\n{nex_song}", parse_mode = "md")
