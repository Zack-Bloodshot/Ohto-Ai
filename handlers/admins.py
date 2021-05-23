from asyncio.queues import QueueEmpty
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

@Client.on_message(filters.command(["auth", "auth@OhtoAiPlaysBot"]) & other_filters)
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

@Client.on_message(filters.command(["remauth", "remauth@OhtoAiPlaysBot"]) & other_filters)
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


@Client.on_message(filters.command(["listauth", "listauth@OhtoAiPlaysBot"]) & other_filters)
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
        msg += f"{count}) `{i.user_id}`: (I didn't see him yet in pm )"
    if msg.endswith("approved.\n"):
        message.reply(f"No users are approved in {chat_title}.")
        return ""
    else:
      await message.reply(msg)

@Client.on_message(filters.command(["pause", "pause@OhtoAiPlaysBot"]) & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    if not sql.is_call(message.chat.id):
      return await message.reply("Nuthin playin.... ")
    if (
            message.chat.id not in callsmusic.pytgcalls.active_calls
    ) or (
            callsmusic.pytgcalls.active_calls[message.chat.id] == 'paused'
    ):
        await message.reply_text("Nuthin playing already right now..", parse_mode ="md")
    else:
        callsmusic.pytgcalls.pause_stream(message.chat.id)
        await message.reply_text("Paused.. hek....", parse_mode = "md")


@Client.on_message(filters.command(["resume", "resume@OhtoAiPlaysBot"]) & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    if (
            message.chat.id not in callsmusic.pytgcalls.active_calls
    ) or (
            callsmusic.pytgcalls.active_calls[message.chat.id] == 'playing'
    ):
        await message.reply_text("Nuthin playin right now....", parse_mode = "md")
    else:
        callsmusic.pytgcalls.resume_stream(message.chat.id)
        await message.reply_text("Ahh Party On Again.... yay!!", parse_mode = "md")


@Client.on_message(filters.command(["stop", "stop@OhtoAiPlaysBot"]) & other_filters)
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

        callsmusic.pytgcalls.leave_group_call(message.chat.id)
        sql.set_off(message.chat.id)
        await message.reply_text("Ahh, its peaceful now, Byee[....](https://telegra.ph/file/d3a1925bb934891796b25.mp4)", parse_mode = "md")


@Client.on_message(filters.command(["skip", "skip@OhtoAiPlaysBot"]) & other_filters)
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
          why.pop(0)
        except KeyError:
          why = []
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
                callsmusic.queues.get(message.chat.id)["file_path"]
            )

        await message.reply_text(f"Skipped....!\n{nex_song}", parse_mode = "md")
