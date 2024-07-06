import pyautogui
import cv2
import numpy as np
from PIL import ImageGrab
import time
import os
import threading
import keyboard

# Ensure the data directory exists
os.makedirs('data', exist_ok=True)

# Load templates for different screens or elements
templates = {}
template_dir = 'templates'
for filename in os.listdir(template_dir):
    if filename.endswith('.png'):
        template_name = os.path.splitext(filename)[0]
        templates[template_name] = cv2.imread(os.path.join(template_dir, filename), 0)
        print(f"Loaded template: {template_name}")

# Define constants
SLEEP_THRESHOLD = 60  # 1 minute
SLEEP_DURATION = 5  # Sleep duration in seconds between movements
SCREENSHOT_INTERVAL = 5  # Take screenshot every 5 seconds

# Flag to indicate if the script should stop
stop_flag = False

def stop_replay():
    global stop_flag
    stop_flag = True
    print("Replay stopped by user")

# Listen for the 'k' key to stop the replay
keyboard.add_hotkey('k', stop_replay)

# Function to take a screenshot
def take_screenshot():
    screenshot = ImageGrab.grab()
    screenshot_path = f"data/screenshot_{int(time.time())}.png"
    screenshot.save(screenshot_path)
    print(f"Screenshot saved: {screenshot_path}")

# Function to capture the current screen
def screenshot():
    screen = ImageGrab.grab()
    return np.array(screen)

# Function to match a template in the current screen
def match_template(image, template):
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    print(f"Template match value: {max_val}")
    return max_val, max_loc

# State Machine for handling different screens
class StateMachine:
    def __init__(self, templates):
        self.state = 'main_screen'
        self.templates = templates
        self.template_keys = list(templates.keys())
        self.current_index = 0
        print(f"Initial state: {self.state}")

    def transition(self, new_state):
        print(f"Transitioning from {self.state} to {new_state}")
        self.state = new_state

    def handle_state(self, screenshot):
        try:
            if self.state == 'error_popup':
                self.handle_error_popup(screenshot)
            else:
                self.handle_generic_state(screenshot)
        except Exception as e:
            print(f"Error in state {self.state}: {e}")
            self.transition('main_screen')

    def handle_generic_state(self, screenshot):
        template_name = self.template_keys[self.current_index]
        template = self.templates[template_name]
        print(f"Handling state: {self.state} with template: {template_name}")
        max_val, max_loc = match_template(screenshot, template)
        if max_val > 0.8:
            print(f"Match found for {template_name} at location {max_loc}")
            pyautogui.click(max_loc[0], max_loc[1])  # Example action
            self.current_index = (self.current_index + 1) % len(self.template_keys)
            next_state = self.template_keys[self.current_index]
            self.transition(next_state)
        else:
            print(f"No match found for {template_name}. Transitioning to error_popup")
            self.transition('error_popup')

    def handle_error_popup(self, screenshot):
        template = self.templates.get('error_popup')
        if template is not None:
            print("Handling error popup")
            max_val, max_loc = match_template(screenshot, template)
            if max_val > 0.8:
                print(f"Error popup detected at location {max_loc}")
                pyautogui.click(max_loc[0], max_loc[1])  # Example action to close popup
                self.transition('main_screen')
            else:
                print("Error popup not detected, retrying main screen")
                self.transition('main_screen')
        else:
            print("Error popup template not found, transitioning to main screen")
            self.transition('main_screen')

# Function to replay events
def replay_events():
    state_machine = StateMachine(templates)
    next_screenshot_time = time.time() + SCREENSHOT_INTERVAL
    while not stop_flag:
        screen = screenshot()
        state_machine.handle_state(screen)
        time.sleep(1)  # Adjust the sleep interval as needed

        # Take screenshot at intervals
        current_time = time.time()
        if current_time >= next_screenshot_time:
            take_screenshot()
            next_screenshot_time = current_time + SCREENSHOT_INTERVAL

# Start replaying events in a separate thread to allow hotkey to work
replay_thread = threading.Thread(target=replay_events)
replay_thread.start()

# Keep the main thread alive to listen for the 'k' key to stop
keyboard.wait('k')
stop_replay()
replay_thread.join()

print("Replay script has finished or was stopped.")
