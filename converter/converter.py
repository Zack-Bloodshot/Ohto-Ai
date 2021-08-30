import os
import asyncio
import ffmpeg


async def convert(file_path: str, dell=True) -> str:
    out = os.path.basename(file_path)
    out = out.split(".")
    out[-1] = "raw"
    out = ".".join(out)
    out = os.path.basename(out)
    out = os.path.join("raw_files", out)

    if os.path.isfile(out):
        return out
    #non async ffmpeg
    #ffmpeg.input(file_path
    #).output(
    #  out,
    #  format='s16le',
    #  acodec='pcm_s16le',
    #  ac=2,
    #  ar='48k',
    #  loglevel='error'
    #).overwrite_output().run() 
    #os.remove(file_path)
    
    #async ffmpeg
    proc = await asyncio.create_subprocess_shell(
        f"ffmpeg -y -i {file_path} -f s16le -ac 2 -ar 48000 -acodec pcm_s16le {out}",
        asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    await proc.communicate()
    if dell==True:
      os.remove(file_path)
    return out
