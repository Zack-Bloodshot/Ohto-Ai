#this is beta!! 


from pyrogram import Client 
from config import SESSION_NAME, API_ID, API_HASH

temp = Client(SESSION_NAME, API_ID, API_HASH)

#async def joinchatto(chat_id):
#  async def (client: Client):
#    await client.join_chat(chat_id)
#    return True
  
def temo(): 
  temp.start()
  
def teme(): 
  temp.stop()