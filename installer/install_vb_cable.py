import webview
import os
import zipfile
import requests
import subprocess
import shutil
from pyuac import main_requires_admin

global window
window = None

def click_handler(e):
    if e.get("target").get("attributes").get("data-action") == "install":
        install()
    else:
        global window
        window.destroy()

def install():
    url = "https://download.vb-audio.com/Download_CABLE/VBCABLE_Driver_Pack43.zip"
    
    save_dir = "./VBCABLE_Driver_Pack43"
    os.makedirs(save_dir, exist_ok=True)

    response = requests.get(url)
    with open(os.path.join(save_dir, "VBCABLE_Driver_Pack43.zip"), "wb") as f:
        f.write(response.content)

    with zipfile.ZipFile(os.path.join(save_dir, "VBCABLE_Driver_Pack43.zip"), 'r') as zip_ref:
        zip_ref.extractall(save_dir)

    exe_path = os.path.join(save_dir, "VBCABLE_Setup_x64.exe")

    if os.path.exists(exe_path):
        print(f"Starting {exe_path}...")
        subprocess.run([exe_path], check=True)
    else:
        print(f"{exe_path} not found.")

    try:
        shutil.rmtree(save_dir, ignore_errors=True)
        print("Directory removed successfully.")
    except Exception as e:
        print(f"Failed to remove directory: {e}")

    print("Process completed.")
    
    global window
    window.destroy()

def bind(window):
    install_button = window.dom.get_element('.install')
    ignore_button = window.dom.get_element('.ignore')

    install_button.events.click += click_handler
    ignore_button.events.click += click_handler

@main_requires_admin
def install_window():
    global window
    window = webview.create_window(
        'Virtual Audio Cable Install', 
        html="""
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Styled Page</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            padding: 20px;
            background-color: #f0f0f0;
        }
        h1 {
            color: #333;
        }
       .button-container {
            display: flex;
            justify-content: space-between;
            margin-top: 20px;
        }
        button {
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button.install {
            background-color: #4CAF50; /* Green */
            color: white;
        }
        button.ignore {
            background-color: #f44336; /* Red */
            color: white;
        }
    </style>
</head>
<body>

<h1>Welcome to My Website</h1>
<p>This is a sample text on my website.</p>

<div class="button-container">
    <button class="install" data-action="install">Install</button>
    <button class="ignore" data-action="ignore">Ignore</button>
</div>

</body>
</html>

        """, draggable=False, resizable=False
    )
    webview.start(bind, window)
