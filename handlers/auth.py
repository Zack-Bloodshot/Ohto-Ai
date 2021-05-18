#DontKnowWhoRU 
from pyrogram import Client, filters 
from pyrogram.types import Message
from helpers.filters import command, other_filters
from helpers.decorators import errors, authorized_users_only
 
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
