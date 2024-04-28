import pystray
from PIL import Image
import subprocess
import asyncio
from pyatv import scan, connect
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import sys

#TODO: ADD SOUND RETURNING TO DEFAULT

ONE_TIME_VOLUME_CHANGE = False
STOP = False

VOLUME_SYNCED_DEVICES = []
CONNECTED_DEVICES = []

PROCESS_PID_POOL = []

class Connected_HomePod:
    def __init__(self, device):
        self.device = device
        self.name = self.device.name
        self.is_connected = False
        self.is_volume_synced = False
        self.process = None
        self.connection = asyncio.run(connect(self.device, asyncio.new_event_loop()))

    def set_volume(self):
        return self.connection

    def toggle_connection(self):
        self.is_connected = not self.is_connected

    def toggle_volume_sync(self):
        self.is_volume_synced = not self.is_volume_synced

async def scan_for_home_pods():
    devices = await scan(loop=asyncio.get_event_loop())
    filter_devices = []
    if not devices:
        print("No HomePods found on the network.")
        exit(1)
    else:
        for device in devices:
            if str(device.device_info).__contains__("HomePod"):
                filter_devices.append(device)
    sorted_devices = sorted(filter_devices, key=lambda device: device.name)
    return sorted_devices

def rescan_devices(old_icon):
    devices = asyncio.run(scan_for_home_pods())
    icon = create_tray_icon(devices)
    icon.run_detached()
    old_icon.stop()

def add_seleted_device_to_audio_stream(name):
    device_states[name].toggle_connection()
    CONNECTED_DEVICES.append(device_states[name])

def add_seleted_device_to_volume_sync(icon, item):
    global ONE_TIME_VOLUME_CHANGE
    ONE_TIME_VOLUME_CHANGE = True
    device_states[item.__name__].toggle_volume_sync()
    VOLUME_SYNCED_DEVICES.append(device_states[item.__name__])
    
def create_tray_icon():
    image = Image.open( __file__[:-7] + "\\trayicon.png") # Replace 'icon.png' with your icon file
    icon = pystray.Icon("name", image, "WinPlay", menu=None)
        
    global device_states
    device_states = {device.name: Connected_HomePod(device) for device in devices}
    
    devices_connected_sub_menue = []
    devices_volume_synced_sub_menue = []
    
    for device in devices:
        devices_connected_sub_menue.append(pystray.MenuItem(device.name, lambda icon, item: start_audio_stream(str(item)), checked=lambda item: device_states[item.__name__].is_connected))
        devices_volume_synced_sub_menue.append(pystray.MenuItem(device.name, lambda icon, item: add_seleted_device_to_volume_sync(icon, item), checked=lambda item: device_states[item.__name__].is_volume_synced))

    menu = (
        pystray.MenuItem(text='Rescan Devices', action=lambda: rescan_devices(icon)),
        pystray.MenuItem('Devices', pystray.Menu(lambda: devices_connected_sub_menue)),
        pystray.MenuItem('Volume Sync', pystray.Menu(lambda: devices_volume_synced_sub_menue)),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem(text='Quit', action=lambda icon: stop(icon)),
    )
    
    icon = pystray.Icon("name", image, "WinPlay", menu=menu)
    return icon

def start_audio_stream(name):
    if device_states[name].is_connected != True:
        add_seleted_device_to_audio_stream(name)
        process = subprocess.Popen([sys.executable, __file__[:-7] + "/audio_stream.py", name])
        device_states[name].process = process
    else:
        device_states[name].process.kill()
        device_states[name].process = None
        device_states[name].toggle_connection()

async def check_volume():
    try:
        print("Master volume listener started")
        audio_devices = AudioUtilities.GetSpeakers()
        interface = audio_devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        prev = volume.GetMasterVolumeLevelScalar()*100
        global ONE_TIME_VOLUME_CHANGE
        while not STOP:
            if (round(volume.GetMasterVolumeLevelScalar()*100) != prev) or ONE_TIME_VOLUME_CHANGE:
                print("Changed master volume level")
                for sync_device in VOLUME_SYNCED_DEVICES:
                    atv = await connect(sync_device.device, asyncio.get_event_loop())
                    audio = atv.audio
                    await audio.set_volume(round(volume.GetMasterVolumeLevelScalar()*100))
                ONE_TIME_VOLUME_CHANGE = False
            prev = round(volume.GetMasterVolumeLevelScalar()*100)
            await asyncio.sleep(1)
        print("Master volume listener stopped")
    except Exception as e:
        print("Error:", e)

def stop(icon):
    global STOP
    STOP = True
    for device_state in device_states.values():
        if device_state.process:
            device_state.process.kill()
    icon.stop()

global devices
devices = asyncio.run(scan_for_home_pods())
icon = create_tray_icon()
icon.run_detached()
asyncio.run(check_volume())
