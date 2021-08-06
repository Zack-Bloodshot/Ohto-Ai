import os

import youtube_dl
from youtube_search import YoutubeSearch
import requests

from helpers.filters import command, other_filters2
from helpers.decorators import errors
from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Voice

from config import BOT_NAME as bn
from config import START_PIC as sp 

@Client.on_message(command("start") & other_filters2)
async def start(_, message: Message):
    await message.reply_text(
        f'I am **{bn}** !! I can play music for you in your voice chat!!, send /help for command list...\n[....]({sp})', parse_mode = "markdown", 
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Deploy me", url="https://heroku.com/deploy?template=https://github.com/Zack-Bloodshot/Ohto-Ai"
                    )],[
                    InlineKeyboardButton(text = "Creator", url = "https://t.me/DontKnowWhyRU"), InlineKeyboardButton(text = "Repo", url = "https://github.com/Zack-Bloodshot/Ohto-Ai")]
            ]
        )
    )

@Client.on_message(command("help") & other_filters2)
@errors
async def help(client, message: Message):
  text = f"I help ya all to play music!!\n\n Use inline mode to play, it makes things easier for you and me, i will search the song and on tapping a result it will initiate play! \n\nThe commands i  currently support are:\n/play - Play the replied song or the youtube url given..\n/song - Upload the searched song in the chat..\n/pause - pause the song\n/resume - resumes music \n/skip - skips to the next song\n/stop - stops the playback and clears queue \n/queue - to get the queue in your pm\n/now - get the currently playing song, can be used by anyone\n/reset - use this to reset everything, use when bot misfunctions[    ..      ]({sp})"
  await message.reply_text(text, parse_mode = "md")
  
@Client.on_message(command("song") & other_filters2)
@errors
async def a(client, message: Message):
    audio_file = None
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    okvai = query.capitalize()
    print(query.capitalize())
    m = await message.reply(f"*🔍 Searching for {okvai}**", parse_mode="md")
    ydl_opts = {
      "format": "bestaudio",
      "addmetadata": True,
      "geo-bypass": True,
      "nocheckcertificate": True,
      "outtmpl": "%(id)s.mp3",
      'forceip' : 4,
    }
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        # results = YoutubeSearch(query, max_results=1).to_dict()
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]

            views = results[0]["views"]
            thumb_name = f'thumb{message.message_id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            await m.edit(f"Found nothing. Try changing the spelling a little.\n\n{e}")
            return
    except Exception as e:
        await m.edit(
           f"Found Nothing. Sorry.\n\nTry another keywork or maybe spell it properly."
        )
        print(str(e))
        return
    await m.edit(f"Downloadingm hehe have patience...\nQuery :- {okvai}")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f' (^_-)\nTitle: [{title[:35]}]({link})\n⏳ *uration:  {duration}\n'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        await  message.reply_audio(audio_file, caption=rep, parse_mode='md',quote=False, title=title, duration=dur, thumb=thumb_name)
        await m.delete()
    except Exception as e:
      print(e)
      await m.edit(f"❌ Error!! \n\n{e}")
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
