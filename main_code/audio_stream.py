import sys
import asyncio
from pyatv import scan
import asyncio.subprocess as asp
from pyatv import scan, connect
from pyatv.const import Protocol

async def scan_dev():
    devices = await scan(loop=asyncio.get_event_loop())
    return devices

async def play_stream_async(device_name):
    print("Connected to:", device.name)
    if device.name == device_name:
        atv = await connect(device, asyncio.get_event_loop())
    
        from pyatv.interface import MediaMetadata

        metadata = MediaMetadata(artist="Windows", title="Streaming windows system audio")
    
        process = await asp.create_subprocess_exec(
            "C:\\Program Files\\ffmpeg\\ffmpeg.exe",
            "-f", "dshow", "-i", "audio=Home Pod (VB-Audio Virtual Cable)",
            "-acodec", "libmp3lame", "-f", "mp3", "-", "-v", "quiet", stdout=asp.PIPE, stderr=None
        )

        await atv.stream.stream_file(process.stdout, metadata=metadata, override_missing_metadata=True)

if len(sys.argv) > 1:
    device_name = sys.argv[1]
    devices = asyncio.run(scan_dev())
    for device in devices:
        if device.name == device_name:
            asyncio.run(play_stream_async(device.name))
else:
    print("No argument was passed.")
