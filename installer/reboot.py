import subprocess
import webview

def reboot_windows():
    """
    Reboots the Windows machine.
    """
    try:
        # Construct the shutdown command to reboot the computer
        command = "shutdown /r /t 0"
        
        # Execute the command
        subprocess.run(command, shell=True, check=True)
        print("Reboot initiated. Please wait for the reboot to complete.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to reboot Windows: {e}")
        
global window
window = None

def click_handler(e):
    if e.get("target").get("attributes").get("data-action") == "install":
        reboot_windows()
    else:
        global window
        window.destroy()


def bind(window):
    install_button = window.dom.get_element('.install')
    ignore_button = window.dom.get_element('.ignore')

    install_button.events.click += click_handler
    ignore_button.events.click += click_handler

def reboot_window():
    global window
    window = webview.create_window(
        'Reboot', 
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
            background-color: #f0f0f0;
            overflow: hidden;
        }
        h1 {
            color: #333;
        }
        
        .text-container {
            height: 85vh;
            overflow-y: auto;
            overflow-x: hidden;
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
    <div class="cont">
<div class="text-container">
<h1>Do you want to Rebbot?</h1>
<p>You have to reboot your PC, because new software has been installed. In order to ensure that everything is working a reboot is required.</p>
</div>
<div class="button-container">
    <button class="install" data-action="install">Reboot</button>
    <button class="ignore" data-action="ignore">Reboot Later</button>
</div>
</div>
</body>
</html>

        """, draggable=False, resizable=False
    )
    webview.start(bind, window)

reboot_window()