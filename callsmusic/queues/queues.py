from asyncio import Queue, QueueEmpty as Empty
from typing import Dict, Union
from sql import calls as sql

queues: Dict[int, Queue] = {}


async def put(chat_id: int, **kwargs) -> int:
    if chat_id not in queues:
        queues[chat_id] = Queue()
    await queues[chat_id].put({**kwargs})
    return queues[chat_id].qsize()

def get(chat_id: int) -> Union[Dict[str, str], None]:
    if chat_id in queues:
        try:
            return queues[chat_id].get_nowait()
        except Empty:
            return None


def is_empty(chat_id: int) -> bool:
    if chat_id in queues:
        return queues[chat_id].empty()
    return True


def task_done(chat_id: int):
    if chat_id in queues:
        try:
            queues[chat_id].task_done()
        except ValueError:
            pass

def clear(chat_id: int):
  if chat_id in queues: 
    for _ in range(queues[chat_id].qsize()):
      queues[chat_id].get_nowait()
      queues[chat_id].task_done()
                       
