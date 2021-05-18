from asyncio.queues import QueueEmpty

from pyrogram import Client, filters 
from pyrogram.types import Message
import callsmusic

from config import BOT_NAME as BN
from config import SUDO_USERS
from helpers.filters import command, other_filters
from helpers.decorators import errors, authorized_users_only
from handlers.play import quu 

auth = []

@Client.on_message(filters.command(["auth", "auth@OhtoAiPlaysBot"]) & other_filters) 
@errors 
@authorized_users_only
async def aauth(client: Client, message: Message):
  user = message.reply_to_message.from_user
  if not user:
    return await message.reply("Reply to a user baka!")
  if user.id in auth:
    await message.reply(f"{user.first_name} is already authorized")
    return
  auth.append(user.id)
  await client.send_message(-1001418899867, auth)
  await message.reply(f"{user.first_name} was authorized to use my commands")
 
@Client.on_message(filters.command(["remauth", "remauth@OhtoAiPlaysBot"]) & other_filters) 
@errors 
@authorized_users_only
async def rauth(client: Client, message: Message):
  reply = message.reply_to_message
  if not reply:
    return await message.reply("Reply to a user baka!")
  user = reply.from_user
  if not user.id in auth:
    await message.reply(f"[{user.first_name}](tg://user?id={user.id}) is already unauthorized", parse_mode = "md")
    return
  auth.remove(user.id)
  await client.send_message(-1001418899867, auth)
  await message.reply(f"[{user.first_name}](tg://user?id={user.id}) was unauthorized to use my commands", parse_mode = "md")
 
  
@Client.on_message(filters.command(["listauth", "listauth@OhtoAiPlaysBot"]) & other_filters) 
@errors 
@authorized_users_only
async def lauth(client: Client, message: Message):
  text = ""
  count = 0
  for user in auth:
    count += 1
    text += count 
    text += f"`{user}`\n"
  await message.reply(text)
 
@Client.on_message(filters.command(["reload", "reload@OhtoAiPlaysBot"]) & other_filters) 
@errors
@authorized_users_only 
async def rload(client: Client, message: Message):
  count = 0
  async for msg in client.search(-1001418899867):
    if count == 1:
      break 
    auth = msg.text
    count = 1 
  await message.reply("Reloaded Successfully ^_^!!! ")

@Client.on_message(filters.command(["pause", "pause@OhtoAiPlaysBot"]) & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
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
    try:
      quu[message.chat.id] = [] 
    except KeyError:
      why = []
    if message.chat.id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("Nuthin Streamin'....... ig so.. ", parse_mode = "md")
    else:
        try:
            callsmusic.queues.clear(message.chat.id)
        except QueueEmpty:
            pass

        callsmusic.pytgcalls.leave_group_call(message.chat.id)
        await message.reply_text("Ahh, its peaceful now, Byee[....](https://telegra.ph/file/d3a1925bb934891796b25.mp4)", parse_mode = "md")


@Client.on_message(filters.command(["skip", "skip@OhtoAiPlaysBot"]) & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    if message.chat.id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("Ahh baka, Nuthin even playin..... ",parse_mode = "md")
    else:
        callsmusic.queues.task_done(message.chat.id)
        try:
          why = quu[message.chat.id]
        except KeyError:
          why = []
        why.pop(0)
        if callsmusic.queues.is_empty(message.chat.id):
            nex_song = " "
            callsmusic.pytgcalls.leave_group_call(message.chat.id)
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
