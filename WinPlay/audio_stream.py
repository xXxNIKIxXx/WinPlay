import sys
import asyncio
from pyatv import scan
import asyncio.subprocess as asp
from pyatv import scan, connect
from pyatv.const import Protocol

from install_vb_cable import install_window

import pyaudio

# Initialize PyAudio
p = pyaudio.PyAudio()

vb_cables_devices = []

# List all available input devices
for i in range(p.get_device_count()):
    device_info = p.get_device_info_by_index(i)
    if device_info['maxInputChannels'] > 0:
        if device_info['name'].__contains__("(VB-Audio Virtual Cable)"):
            vb_cables_devices.append(device_info['name'])

vb_cables_devices = list(set(vb_cables_devices))


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
            "ffmpeg",
            "-f", "dshow", "-i", "audio=" + vb_cables_devices[0] + "",
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
