from pyrogram import Client
from pyrogram.utils import MAX_CHANNEL_ID
from pytgcalls import GroupCallFactory
import config
from . import queues
from sql import calls as sql
import asyncio

client = Client(config.SESSION_NAME, config.API_ID, config.API_HASH)
quu = {} 

GROUP_CALL = {}

class Music(object):
    
  async def call(chat_id):
    if chat_id in GROUP_CALL:
      return GROUP_CALL[chat_id]
    else:
      gp = GroupCallFactory(client).get_file_group_call()
      await gp.start(chat_id)
      GROUP_CALL[chat_id] = gp
      return gp
  
  async def leave(chat_id):
    if chat_id in GROUP_CALL:
      group_call = GROUP_CALL[chat_id]
      await group_call.stop()
      GROUP_CALL.pop(chat_id)

mp = Music()

@mp.group_call.on_playout_ended
async def on_stream_end(context):
    chat_id = MAX_CHANNEL_ID - context.full_chat.id
    queues.task_done(chat_id)

    if queues.is_empty(chat_id):
        await mp.leave(chat_id)
        sql.set_off(chat_id)
        
    else:
        quu[chat_id].pop(0)
        mp.group_call.input_filename = queues.get(chat_id)["file_path"]
        try:
          send_now_playing(chat_id)
        except Exception as e:
          print(e)

run = client.run