import os
import asyncio
import ffmpeg

from helpers.errors import FFmpegReturnCodeError


async def convert(file_path: str) -> str:
    out = os.path.basename(file_path)
    out = out.split(".")
    out[-1] = "raw"
    out = ".".join(out)
    out = os.path.basename(out)
    out = os.path.join("raw_files", out)

    if os.path.isfile(out):
        return out

    ffmpeg.input(file_path
    ).output(
      out,
      format='s16le',
      acodec='pcm_s16le',
      ac=2,
      ar='48k',
      loglevel='error'
    ).overwrite_output().run() 
    os.remove(file_path)
    return out
