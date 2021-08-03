from os import path
import asyncio
import ffmpeg

from helpers.errors import FFmpegReturnCodeError


async def convert(file_path: str) -> str:
    out = path.basename(file_path)
    out = out.split(".")
    out[-1] = "raw"
    out = ".".join(out)
    out = path.basename(out)
    out = path.join("raw_files", out)

    if path.isfile(out):
        return out

    ffmpeg.input(file_path
    ).output(
      out,
      format='s16le',
      acodec='pcm_s16le',
      ac=2,
      ar='48k',
      oglevell='error'
    ).overwrite_output().run() 
    os.remove(file_path)
    return out
