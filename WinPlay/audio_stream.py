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
    if result.stderr.split("\n")[i].__contains__("(VB-Audio Virtual Cable)"):
        output_device = result.stderr.split("\n")[i+1].split('"')[1]


async def scan_dev():
    devices = await scan(loop=asyncio.get_event_loop())
    return devices

async def play_stream_async(device_name):
    print("Connected to:", device.name)
    if device.name == device_name:
        atv = await connect(device, asyncio.get_event_loop())
        

        print(output_device)
        process = await asp.create_subprocess_exec(
            "ffmpeg",
            "-f", "dshow", "-i", "audio=" + "@device_cm_{33D9A762-90C8-11D0-BD43-00A0C911CE86}\wave_{7BA32019-AD16-44D6-9403-721012116A7B}",
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
