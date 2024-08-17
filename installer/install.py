#from install_ffmpeg import install
#from install_vb_cable import install_window
#from reboot import reboot_window



import subprocess

def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg"])
        return True
    except FileNotFoundError:
        print("Not installed")
        return False

def check_vb_cable():
    return True

ffmpge_inst = check_ffmpeg()

#install_window()
#install()
#reboot_window()