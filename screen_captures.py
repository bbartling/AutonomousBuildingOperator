import pyautogui
import json
import time
import threading
import keyboard
import os
from PIL import ImageGrab

# Ensure the data directory exists
os.makedirs('data', exist_ok=True)

# Load events from the file
with open('mouse_events.json', 'r') as f:
    events = json.load(f)

# Define the sleep threshold in seconds (e.g., 1 minute)
SLEEP_THRESHOLD = 60  # 1 minute
SLEEP_DURATION = 5  # Sleep duration in seconds between movements
screenshot_interval = 5  # Take screenshot every 5 seconds

# Flag to indicate if the script should stop
stop_flag = False

def stop_replay():
    global stop_flag
    stop_flag = True
    print("Replay stopped")

# Listen for the 'k' key to stop the replay
keyboard.add_hotkey('k', stop_replay)

# Function to take a screenshot
def take_screenshot():
    screenshot = ImageGrab.grab()
    screenshot.save(f"data/screenshot_{int(time.time())}.png")

# Function to replay events
def replay_events():
    global stop_flag
    while not stop_flag:
        start_time = events[0][3]
        next_screenshot_time = start_time + screenshot_interval
        
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

            # Take screenshot if the interval has passed
            if timestamp >= next_screenshot_time:
                take_screenshot()
                next_screenshot_time = timestamp + screenshot_interval

            time.sleep(timestamp - start_time)
            start_time = timestamp

# Start replaying events in a separate thread to allow hotkey to work
replay_thread = threading.Thread(target=replay_events)
replay_thread.start()

# Keep the main thread alive to listen for the 'k' key to stop
keyboard.wait('k')
stop_replay()
replay_thread.join()

print("Replay script has finished or was stopped.")
