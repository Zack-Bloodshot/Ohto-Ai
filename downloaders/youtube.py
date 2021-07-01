from os import path 
import os
from youtube_dl import YoutubeDL
from pytube import YouTube as YT
from config import BOT_NAME as bn, DURATION_LIMIT
from helpers.errors import DurationLimitError

ydl_opts = {
    "format": "bestaudio",
    "addmetadata": True,
    "geo-bypass": True,
    "nocheckcertificate": True,
    "outtmpl": "downloads/%(id)s.%(ext)s",
}
ydl = YoutubeDL(ydl_opts)


def download(url: str) -> str:
    yt = YT(url)
    yl = yt.streams.get_audio_only()
    duration = round(yt.length / 60)

    if duration > DURATION_LIMIT:
        raise DurationLimitError(
            f"Videos longer than {DURATION_LIMIT} minute(s) aren't allowed, the provided video is {duration} minute(s)"
        )

    dl = yl.download()
    path, ext = os.path.splitext(dl)
    file_name = path + '.m4a'
    dl = os.rename(dl, file_name)
    return os.path.join("downloads", dl)
