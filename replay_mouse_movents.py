import pyautogui
import json
import time

# Load events from the file
with open('mouse_events.json', 'r') as f:
    events = json.load(f)

# Replay events
start_time = events[0][3]
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
    start_time = timestamp
