from asyncio.queues import QueueEmpty
from datetime import datetime as kek
from sql import calls as sql
from pyrogram import Client, filters 
from pyrogram.types import Message, Chat, User
import callsmusic
from pyrogram.errors import PeerIdInvalid
from sql import auth as ats
from config import BOT_NAME as BN
from config import SUDO_USERS
from helpers.filters import command, other_filters
from helpers.decorators import errors, authorized_users_only, authorized_users_only2
from handlers.play import quu 
from config import BOT_USERNAME
from config import PLAY_PIC 
from config import UBOT_ID as ubot

@Client.on_message(filters.command(["summon", f"summon@{BOT_USERNAME}"]))
@authorized_users_only2
async def summon(client: Client, message: Message): 
  m = message.reply("Yea well, waitto, will take some time!")
  await joinchatto(int(message.chat.id))
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
    callsmusic.pytgcalls.leave_group_call(message.chat.id) 
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

@Client.on_message(filters.command(["remauth", f"remauth@{BOT_USERNAME}"]) & other_filters)
@errors 
@authorized_users_only 
async def remauth(_, message: Message): 
  reply = message.reply_to_message
  if not reply: 
    return await message.reply("Reply To a user to unauthorize.. ")
  user = reply.from_user
  if ats.is_approved(message.chat.id, user.id):
    ats.disapprove(message.chat.id, user.id)
    await message.reply(f"[{user.first_name}](tg://user?id={user.id}) was removed from authorized list..")
  else: 
    return await message.reply(f"[{user.first_name}](tg://user?id={user.id}) is already not authorized..")

async def meme_get(chat: Chat, user): 
  return await chat.get_member(user)


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
    if callsmusic.pytgcalls.active_calls[message.chat.id] == 'paused':
        await message.reply_text("Nuthin playing already right now..", parse_mode ="md")
    else:
        callsmusic.pytgcalls.pause_stream(message.chat.id)
        await message.reply_text("Paused.. hek....", parse_mode = "md")


@Client.on_message(filters.command(["resume", f"resume@{BOT_USERNAME}"]) & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    if not sql.is_call(message.chat.id):
      return await message.reply("Nuthin playin...")
    if callsmusic.pytgcalls.active_calls[message.chat.id] == 'playing':
        await message.reply_text("Already playing!!", parse_mode = "md")
    else:
        callsmusic.pytgcalls.resume_stream(message.chat.id)
        await message.reply_text("Ahh Party On Again.... yay!!", parse_mode = "md")


@Client.on_message(filters.command(["stop", f"stop@{BOT_USERNAME}"]) & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    if not sql.is_call(message.chat.id):
        await message.reply_text("Nuthin Streamin'....... ig so.. ", parse_mode = "md")
    else:
        try: 
          callsmusic.queues.clear(message.chat.id)
        except QueueEmpty: 
          pass 
        quu[message.chat.id] = []
        callsmusic.pytgcalls.leave_group_call(message.chat.id)
        sql.set_off(message.chat.id)
        await message.reply_text(f"Ahh, its peaceful now, Byee[...]({PLAY_PIC})", parse_mode = "md")


@Client.on_message(filters.command(["skip", f"skip@{BOT_USERNAME}"]) & other_filters)
@errors
@authorized_users_only2
async def skip(_, message: Message):
    if not sql.is_call(message.chat.id):
      return await message.reply("Baka nothing to skip..!")
    if callsmusic.queues.is_empty(message.chat.id):
      try:
        callsmusic.pytgcalls.leave_group_call(message.chat.id) 
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
            callsmusic.pytgcalls.leave_group_call(message.chat.id)
            sql.set_off(message.chat.id)
        else:
            try:
              nex_song = "**Now playin: " + why[0] + "**"
            except IndexError:
              nex_song = " "
            callsmusic.pytgcalls.change_stream(
                message.chat.id,
                callsmusic.queues.get(message.chat.id)["file_path"])

        await message.reply_text(f"Skipped....!\n{nex_song}", parse_mode = "md")
