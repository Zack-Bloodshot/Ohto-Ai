#calls sql.. 
import threading

from sql import BASE, SESSION
from sqlalchemy import Column, String


class Pykall(BASE):
    __tablename__ = "vconchats"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id


Pykall.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()


def is_call(chat_id): 
  try:
    chat = SESSION.query(Pykall).get(str(chat_id))
    if chat:
      return True
    else:
      return False 
  finally:
    SESSION.close()

def set_on(chat_id):
  with INSERTION_LOCK:
    vc_on = SESSION.query(Pykall).get(str(chat_id))
    if not vc_on:
      vc_on = Pykall(str(chat_id))
    else:
      pass
    SESSION.add(vc_on)
    SESSION.commit()

def set_off(chat_id):
  with INSERTION_LOCK:
   vc_on = SESSION.query(Pykall).get(str(chat_id))
   if vc_on:
     SESSION.delete(vc_on)
   SESSION.commit()

def get_vc_on(chat_id):
  try:
    return SESSION.query(Pykall.chat_id).all()
  finally:
    SESSION.close()


