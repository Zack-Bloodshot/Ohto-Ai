#playlist toggle 
import threading

from sql import BASE, SESSION
from sqlalchemy import Column, String


class Playlist(BASE):
    __tablename__ = "playliston"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id


Playlist.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()


def is_playlist_on(chat_id): 
  try:
    chat = SESSION.query(Playlist).get(str(chat_id))
    if chat:
      return True
    else:
      return False 
  finally:
    SESSION.close()

def set_playlist_on(chat_id):
  with INSERTION_LOCK:
    play_on = SESSION.query(Playlist).get(str(chat_id))
    if not play_on:
      play_on = Playlist(str(chat_id))
    else:
      pass
    SESSION.add(vc_on)
    SESSION.commit()

def set_playlist_off(chat_id):
  with INSERTION_LOCK:
   play_on = SESSION.query(Playlist).get(str(chat_id))
   if play_on:
     SESSION.delete(play_on)
   SESSION.commit()

def get_plyalist_on(chat_id):
  try:
    return SESSION.query(Playlist .chat_id).all()
  finally:
    SESSION.close()




