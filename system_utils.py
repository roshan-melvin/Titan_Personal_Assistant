import os
import wmi
import psutil
import tkinter as tk
from tkinter import simpledialog, messagebox
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math

# Audio functions
def dB_to_linear(dB):
    """Convert decibels to linear scale."""
    return 10 ** (dB / 20.0)

def linear_to_dB(linear):
    """Convert linear scale to decibels."""
    if linear <= 0:
        return -96.0  # Minimum dB value
    return 20 * math.log10(linear)

def set_system_volume(level):
    """Set system volume to a specific level (0-100)."""
    level = max(0, min(100, level))
    linear_volume = level / 100.0
    volume_dB = linear_to_dB(linear_volume)
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume_control = cast(interface, POINTER(IAudioEndpointVolume))
        volume_control.SetMasterVolumeLevel(volume_dB, None)
        print(f"Volume set to {level}% ({volume_dB:.2f} dB)")
        return True
    except Exception as e:
        print(f"Error setting volume: {e}")
        return False

def get_current_volume():
    """Get the current system volume level (0-100)."""
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume_control = cast(interface, POINTER(IAudioEndpointVolume))
        current_volume_dB = volume_control.GetMasterVolumeLevel()
        current_volume_linear = dB_to_linear(current_volume_dB)
        return int(current_volume_linear * 100)
    except Exception as e:
        print(f"Error getting current volume: {e}")
        return 50

def mute_system_volume():
    """Mute the system volume."""
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume_control = cast(interface, POINTER(IAudioEndpointVolume))
        volume_control.SetMute(True, None)
        print("Volume muted.")
        return True
    except Exception as e:
        print(f"Error muting volume: {e}")
        return False

def unmute_system_volume():
    """Unmute the system volume."""
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume_control = cast(interface, POINTER(IAudioEndpointVolume))
        volume_control.SetMute(False, None)
        print("Volume unmuted.")
        return True
    except Exception as e:
        print(f"Error unmuting volume: {e}")
        return False

def increase_volume(amount):
    """Increase system volume by the specified amount."""
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume_control = cast(interface, POINTER(IAudioEndpointVolume))

        current_volume = get_current_volume()
        new_volume = max(0, min(100, current_volume + amount))
        volume_control.SetMasterVolumeLevelScalar(new_volume / 100.0, None)

        print(f"Volume increased to {new_volume}%")
        return True
    except Exception as e:
        print(f"Error increasing volume: {e}")
        return False

def decrease_volume(amount):
    """Decrease system volume by the specified amount."""
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume_control = cast(interface, POINTER(IAudioEndpointVolume))

        current_volume = get_current_volume()
        new_volume = max(0, min(100, current_volume - amount))
        volume_control.SetMasterVolumeLevelScalar(new_volume / 100.0, None)

        print(f"Volume decreased to {new_volume}%")
        return True
    except Exception as e:
        print(f"Error decreasing volume: {e}")
        return False

# Brightness functions
def set_brightness(level):
    """Set screen brightness to a specific level (0-100)."""
    level = max(0, min(100, level))
    try:
        c = wmi.WMI(namespace='wmi')
        methods = c.WmiMonitorBrightnessMethods()[0]
        methods.WmiSetBrightness(level, 0)
        print(f"Brightness set to {level}%")
        return True
    except Exception as e:
        print(f"Error setting brightness: {e}")
        return False

def get_current_brightness():
    """Get the current screen brightness level (0-100)."""
    try:
        c = wmi.WMI(namespace='wmi')
        brightness = c.WmiMonitorBrightness()[0].CurrentBrightness
        print(f"Current brightness level: {brightness}%")
        return brightness
    except Exception as e:
        print(f"Error getting current brightness: {e}")
        return 50

# System functions
def connect_to_wifi(ssid, password):
    """Connect to a Wi-Fi network with the given SSID."""
    try:
        command = f'netsh wlan connect name="{ssid}"'
        result = os.system(command)
        return result == 0
    except Exception as e:
        print(f"Error connecting to Wi-Fi: {e}")
        return False

def shutdown_system():
    """Shutdown the system."""
    try:
        os.system("shutdown /s /t 1")
        return True
    except Exception as e:
        print(f"Error shutting down system: {e}")
        return False

def reboot_system():
    """Reboot the system."""
    try:
        os.system("shutdown /r /t 1")
        return True
    except Exception as e:
        print(f"Error rebooting system: {e}")
        return False

def show_battery_percentage():
    """Get battery status information."""
    try:
        battery = psutil.sensors_battery()
        if battery is not None:
            percent = battery.percent
            plugged_in = "Plugged in" if battery.power_plugged else "Not plugged in"
            return f"The battery is at {percent}% ({plugged_in})"
        else:
            return "Battery information not available."
    except Exception as e:
        print(f"Error getting battery status: {e}")
        return "Unable to retrieve battery information."

# GUI Functions
def get_wifi_credentials():
    """
    Show a GUI dialog to get Wi-Fi credentials from the user.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    ssid = simpledialog.askstring("Wi-Fi Name", "Please provide the Wi-Fi name:")
    if not ssid:
        return None, None  # No SSID provided

    password = simpledialog.askstring("Wi-Fi Password", "Please provide the password:", show='*')
    return ssid, password

def open_wifi_gui():
    def connect():
        ssid, password = get_wifi_credentials()
        if ssid and password:
            connect_to_wifi(ssid, password)
            messagebox.showinfo("Success", f"Connecting to Wi-Fi network {ssid}.")
        else:
            messagebox.showwarning("Input Error", "Please enter both SSID and Password.")
    
    root = tk.Tk()
    root.title("Connect to Wi-Fi")
    
    tk.Label(root, text="Click to enter Wi-Fi credentials").pack(padx=20, pady=5)
    
    tk.Button(root, text="Get Credentials and Connect", command=connect).pack(pady=10)
    root.mainloop()

# Main function
def main():
    # Example usage of GUI
    open_wifi_gui()
    
    # Example usage of other functions
    print(show_battery_percentage())

if __name__ == "__main__":
    main()
