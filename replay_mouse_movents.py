import pyautogui
import json
import time
import threading
import keyboard

# Load events from the file
with open('mouse_events.json', 'r') as f:
    events = json.load(f)

# Define the sleep threshold in seconds (e.g., 1 minute)
SLEEP_THRESHOLD = 60  # 1 minute
SLEEP_DURATION = 5  # Sleep duration in seconds between movements

# Flag to indicate if the script should stop
stop_flag = False

def stop_replay():
    global stop_flag
    stop_flag = True
    print("Replay stopped")

# Listen for the 'k' key to stop the replay
keyboard.add_hotkey('k', stop_replay)

# Replay events
start_time = events[0][3]
for event in events:
    if stop_flag:
        break
    
    event_type = event[0]
    timestamp = event[-1]
    elapsed_time = timestamp - start_time
    
    if elapsed_time > SLEEP_THRESHOLD:
        print(f"Sleeping for {SLEEP_DURATION} seconds")
        time.sleep(SLEEP_DURATION)
    
    if event_type == 'move':
        _, x, y, timestamp = event
        pyautogui.moveTo(x, y)
    elif event_type == 'click':
        _, x, y, button, timestamp = event
        pyautogui.click(x, y)
    elif event_type == 'scroll':
        _, x, y, dx, dy, timestamp = event
        pyautogui.scroll(dy, x, y)
    
    time.sleep(timestamp - start_time)
    start_time = timestamp

print("Replay script has finished or was stopped.")
