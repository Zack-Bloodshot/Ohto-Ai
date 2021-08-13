from os import path 
import os
from youtube_dl import YoutubeDL
from pytube import YouTube as YT
from config import BOT_NAME as bn, DURATION_LIMIT, PROXY
from helpers.errors import DurationLimitError

using_proxy = False

if PROXY:
    ydl_opts = {
      "format": "bestaudio",
      "addmetadata": True,
      "geo-bypass": True,
      "nocheckcertificate": True,
      "outtmpl": "downloads/%(id)s.%(ext)s",
      "forceip": 4,
      "proxy:": f'socks5://{PROXY}'
    }
    using_proxy = True
else:
  ydl_opts = {
      "format": "bestaudio",
      "addmetadata": True,
      "geo-bypass": True,
      "nocheckcertificate": True,
      "outtmpl": "downloads/%(id)s.%(ext)s",
      "forceip": 4,
  }

yd = YoutubeDL(ydl_opts)


def download(url: str) -> str:
    global yd
    info = yd.extract_info(url, False)
    duration = round(info['duration'] / 60)

    if duration > DURATION_LIMIT:
        raise DurationLimitError(
            f"Videos longer than {DURATION_LIMIT} minute(s) aren't allowed, the provided video is {duration} minute(s)"
        )
    try:
      yd.download([url])
    except Exception as e:
      if type(e).__name__ == "DownloadError":
        if PROXY:
          if using_proxy == True:
            ydl_opts = {
              "format": "bestaudio",
              "addmetadata": True,
              "geo-bypass": True,
              "nocheckcertificate": True,
              "outtmpl": "downloads/%(id)s.%(ext)s",
              "forceip": 4,
            }
            using_proxy=False
            yd = YoutubeDL(ydl_opts)
            yd.download([url])
          else:
            ydl_opts = {
              "format": "bestaudio",
              "addmetadata": True,
              "geo-bypass": True,
              "nocheckcertificate": True,
              "outtmpl": "downloads/%(id)s.%(ext)s",
              "forceip": 4,
              "proxy:": f'socks5://{PROXY}'
            }
            using_proxy=True 
            yd = YoutubeDL(ydl_opts)
            yd.download([url])
        else:
          yd.download([url])
    return path.join("downloads", f"{info['id']}.{info['ext']}") 
