#DontKnowWhoRU 
from pyrogram import Client, filters 
from pyrogram.types import Message
from helpers.filters import command, other_filters
from config import SUDO_USERS 
from helpers.admins import get_administrators
 
auth = []

#please make a channel and use its id besides my one duh 

@Client.on_message(filters.command(["auth", "auth@OhtoAiPlaysBot"]) & other_filters) 
async def aauth(client: Client, message: Message):
  if not message.from_user.id in SUDO_USERS: 
    return 
  if not message.from_user.id in auth:
    return 
  user = message.reply_to_message.from_user
  if not user:
    return await message.reply("Reply to a user baka!")
  if user.id in auth:
    await message.reply(f"[{user.first_name}](tg://user?id={user.id}) is already authorized", parse_mode = "md")
    return
  auth.append(user.id)
  await client.send_message(-1001418899867, auth)
  await message.reply(f"[{user.first_name}](tg://user?id={user.id}) was authorized to use my commands", parse_mode = "md")
 
@Client.on_message(filters.command(["remauth", "remauth@OhtoAiPlaysBot"]) & other_filters) 
async def rauth(client: Client, message: Message):
  if not message.from_user.id in SUDO_USERS:
    return 
  if not message.from_user.id in auth:
    return 
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
async def lauth(client: Client, message: Message):
  if not message.from_user.id in SUDO_USERS: 
    return 
  if not message.from_user.id in auth:
    return 
  text = ""
  count = 0
  for user in auth:
    count += 1
    text += f"{count}: "
    text += f"`{user}`\n"
  await message.reply(text)
 
@Client.on_message(filters.command(["reload", "reload@OhtoAiPlaysBot"]) & other_filters) 
async def rload(client: Client, message: Message):
  if not message.from_user.id in SUDO_USERS:
    return 
  if not message.from_user.id in auth:
    return 
  count = 0
  admemes = await get_administrators(message.chat)
  async for msg in client.search_messages(-1001418899867):
    if count == 1:
      break 
    auth = msg.text
    count = 1 
  for ad in admemes:
    auth.append(ad)
  await client.send_message(-1001418899867, auth)
  await message.reply("Reloaded Successfully ^_^!!! ")
