from typing import Callable

from pyrogram import Client
from pyrogram.types import Message
from helpers.admins import get_administrators
from config import SUDO_USERS
from sql import auth as sql
import sys, os


def errors(func: Callable) -> Callable:
    async def decorator(client: Client, message: Message):
        try:
            return await func(client, message)
        except Exception as e:
            if type(e).__name__ == "DownloadError":
              await message.reply_text("Ahh sorry looks like i am not being able to download..., please retry again or use telegram files..")
            else: 
              exc_type, exc_obj, exc_tb = sys.exc_info()
              fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
              print(exc_type, fname, exc_tb.tb_lineno)
              msg = f'{exc_type}:\n{e}\nIn file {fname} line {exc_tb.tb_lineno}'
              await message.reply(msg)
              print(e)

    return decorator


def authorized_users_only(func: Callable) -> Callable:
    async def decorator(client: Client, message: Message):
        if message.from_user.id in SUDO_USERS:
            return await func(client, message)
        administrators = await get_administrators(message.chat)
        for administrator in administrators:
            if administrator == message.from_user.id:
                return await func(client, message)

    return decorator

def authorized_users_only2(func: Callable) -> Callable:
    async def decorator(client: Client, message: Message):
        if message.from_user.id in SUDO_USERS:
            return await func(client, message)
        elif sql.is_approved(message.chat.id, message.from_user.id):
            return await func(client, message)
        administrators = await get_administrators(message.chat)
        for admin in administrators:
          if admin == message.from_user.id:
            return await func(client, message)
        return await message.delete()

    return decorator