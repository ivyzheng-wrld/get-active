
import pyautogui
import threading
import time
from datetime import datetime
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw

# Configurable hours (24-hour format)
START_HOUR = 9
END_HOUR = 17
MOVE_INTERVAL = 180  # in seconds (4 minutes)

# Flag to control thread
running = True

def is_within_active_hours():
    now = datetime.now()
    return START_HOUR <= now.hour < END_HOUR

def mouse_mover_loop():
    while running:
        if is_within_active_hours():
            pyautogui.move(50, 0)
            pyautogui.move(-50, 0)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Mouse moved")
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Outside working hours")
        time.sleep(MOVE_INTERVAL)

def create_icon_image():
    # Create a simple black square icon
    image = Image.new('RGB', (64, 64), color='black')
    draw = ImageDraw.Draw(image)
    draw.ellipse((16, 16, 48, 48), fill='white')
    return image

def on_quit(icon, item):
    global running
    running = False
    icon.stop()

def setup_tray_icon():
    menu = Menu(MenuItem('Quit', on_quit))
    icon = Icon("MouseMover", icon=create_icon_image(), menu=menu)
    return icon

if __name__ == "__main__":
    thread = threading.Thread(target=mouse_mover_loop, daemon=True)
    thread.start()

    tray_icon = setup_tray_icon()
    tray_icon.run()
