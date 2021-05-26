from pyrogram import Client 
from config import SESSION_NAME, API_ID, API_HASH

temp = Client(SESSION_NAME, API_ID, API_HASH)

async def joinchatto(client: Client, chat_id):
  await client.join_chat(chat_id)
  return True
  
async def temo(): 
  temp.start()
  
async def teme(): 
  temp.stop()