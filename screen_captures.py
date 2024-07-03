import pyautogui
import json
import time
from PIL import ImageGrab

# Load events from the file
with open('mouse_events.json', 'r') as f:
    events = json.load(f)

# Function to take a screenshot
def take_screenshot():
    screenshot = ImageGrab.grab()
    screenshot.save(f"screenshot_{int(time.time())}.png")

# Replay events and take screenshots at intervals
start_time = events[0][3]
screenshot_interval = 5  # Take screenshot every 5 seconds
next_screenshot_time = start_time + screenshot_interval

for event in events:
    event_type = event[0]
    if event_type == 'move':
        _, x, y, timestamp = event
        time.sleep(timestamp - start_time)
        pyautogui.moveTo(x, y)
    elif event_type == 'click':
        _, x, y, button, timestamp = event
        time.sleep(timestamp - start_time)
        pyautogui.click(x, y)
    elif event_type == 'scroll':
        _, x, y, dx, dy, timestamp = event
        time.sleep(timestamp - start_time)
        pyautogui.scroll(dy, x, y)

    # Take screenshot if the interval has passed
    if timestamp >= next_screenshot_time:
        take_screenshot()
        next_screenshot_time = timestamp + screenshot_interval

    start_time = timestamp
