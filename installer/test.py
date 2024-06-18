import subprocess

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

# Call the function to reboot Windows
reboot_windows()
