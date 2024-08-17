import sys
import asyncio
from pyatv import scan, interface
import asyncio.subprocess as asp
from pyatv import scan, connect
from pyatv.const import Protocol


import subprocess

result = subprocess.run(['ffmpeg', '-list_devices', 'true', '-f', 'dshow', '-i', 'dummy'], capture_output=True, text=True)

output_device = ""

for i in range(len(result.stderr.split("\n"))):
    print(i)
    if result.stderr.split("\n")[i].__contains__("(VB-Audio Virtual Cable)"):
        output_device = result.stderr.split("\n")[i+1].split('"')[1]


async def scan_dev():
    devices = await scan(loop=asyncio.get_event_loop())
    return devices

class MyAudioListener(interface.AudioListener):

    def volume_update(self, old_level, new_level):
        print('Volume level changed from {0:f} to {1:f}'.format(old_level, new_level))

async def play_stream_async(device_name):
    print("Connected to:", device.name)
    if device.name == device_name:
        atv = await connect(device, asyncio.get_event_loop())
        
        listener = MyAudioListener()
        atv.audio.listener = listener
        
        from pyatv.interface import MediaMetadata

        metadata = MediaMetadata(artist="Windows", title="Streaming windows system audio")
        process = await asp.create_subprocess_exec(
            "ffmpeg",
            "-f", "dshow", "-i", "audio=" + output_device,
            "-acodec", "libmp3lame", "-f", "mp3", "-", "-v", "quiet", stdin=None, stdout=asp.PIPE, stderr=None
        )

        await atv.stream.stream_file(process.stdout)

if len(sys.argv) > 1:
    device_name = sys.argv[1]
    devices = asyncio.run(scan_dev())
    for device in devices:
        if device.name == device_name:
            asyncio.run(play_stream_async(device.name))
else:
    print("No argument was passed.")
