import os
import requests
import zipfile
import shutil

def install():
    url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
    
    save_dir = "./ffmpeg-master-latest-win64-gpl"
    os.makedirs(save_dir, exist_ok=True)
    os.makedirs("./ffmpeg", exist_ok=True)
    
    response = requests.get(url)
    with open(os.path.join(save_dir, "ffmpeg-master-latest-win64-gpl.zip"), "wb") as f:
        f.write(response.content)

    with zipfile.ZipFile(os.path.join(save_dir, "ffmpeg-master-latest-win64-gpl.zip"), 'r') as zip_ref:
        zip_ref.extractall(save_dir)
    
    ffmpeg_exe = os.path.join(save_dir, save_dir, "bin", "ffmpeg.exe")
    
    shutil.move(ffmpeg_exe, "./ffmpeg")
    
    
    try:
        shutil.rmtree(save_dir, ignore_errors=True)
        print("Directory removed successfully.")
    except Exception as e:
        print(f"Failed to remove directory: {e}")
    
    print("Process completed.")


install()