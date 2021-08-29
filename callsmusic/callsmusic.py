from pyrogram import Client
from pyrogram import filters
from pyrogram.raw import functions
from pyrogram.utils import MAX_CHANNEL_ID
from pytgcalls import GroupCallFactory
import config
from . import queues
from sql import calls as sql
import asyncio

client = Client(config.SESSION_NAME, config.API_ID, config.API_HASH)
quu = {} 
block_chat = []
GROUP_CALL = {}

async def on_stream_end(context, *args):
    chat_id = MAX_CHANNEL_ID - context.full_chat.id
    queues.task_done(chat_id)

    if queues.is_empty(chat_id):
        await mp.leave(chat_id)
        sql.set_off(chat_id)
        try:
          block_chat.pop(chat_id)
        except Exception:
          pass
        
    else:
        quu[chat_id].pop(0)
        GROUP_CALL[chat_id].input_filename = queues.get(chat_id)["file_path"]
        try:
          send_now_playing(chat_id)
        except Exception as e:
          print(e)
          
def crazy(chat_id):
  if chat_id in GROUP_CALL:
    gp = GROUP_CALL[chat_id]
    gp.on_playout_ended(on_stream_end)

class Music(object):
    
  async def call(self, chat_id):
    if chat_id in GROUP_CALL:
      return GROUP_CALL[chat_id]
    else:
      gp = GroupCallFactory(client,outgoing_audio_bitrate_kbit=320).get_file_group_call()
      await gp.start(chat_id)
      GROUP_CALL[chat_id] = gp
      crazy(chat_id)
      return gp
  
  async def leave(self, chat_id):
    if chat_id in GROUP_CALL:
      group_call = GROUP_CALL[chat_id]
      await group_call.stop()
      GROUP_CALL.pop(chat_id)

mp = Music()

@client.on_message(filters.private)
async def annoy(client, message):
  await message.delete()
  await message.reply_text(f'Baka Im jst a bot,  used to play music, for more check @{config.BOT_USERNAME}!')
  

run = client.run