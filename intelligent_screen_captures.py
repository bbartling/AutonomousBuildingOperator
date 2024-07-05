import pyautogui
import cv2
import numpy as np
from PIL import ImageGrab
import time
import os
import keyboard

# Ensure the data directory exists
os.makedirs('data', exist_ok=True)

# Load templates for different screens or elements
template_main_screen = cv2.imread('templates/main_screen.png', 0)
template_device_screen = cv2.imread('templates/device_screen.png', 0)
template_error_popup = cv2.imread('templates/error_popup.png', 0)

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

# Function to capture the current screen
def screenshot():
    screen = ImageGrab.grab()
    return np.array(screen)

# Function to match a template in the current screen
def match_template(image, template):
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    return max_val, max_loc

# State Machine for handling different screens
class StateMachine:
    def __init__(self):
        self.state = 'MAIN_SCREEN'

    def transition(self, new_state):
        print(f"Transitioning to {new_state}")
        self.state = new_state

    def handle_state(self, screenshot):
        try:
            if self.state == 'MAIN_SCREEN':
                self.handle_main_screen(screenshot)
            elif self.state == 'DEVICE_SCREEN':
                self.handle_device_screen(screenshot)
            elif self.state == 'ERROR_POPUP':
                self.handle_error_popup(screenshot)
        except Exception as e:
            print(f"Error in state {self.state}: {e}")
            self.transition('MAIN_SCREEN')

    def handle_main_screen(self, screenshot):
        max_val, max_loc = match_template(screenshot, template_main_screen)
        if max_val > 0.8:
            pyautogui.click(max_loc[0], max_loc[1])  # Example action
            self.transition('DEVICE_SCREEN')
        else:
            self.transition('ERROR_POPUP')

    def handle_device_screen(self, screenshot):
        max_val, max_loc = match_template(screenshot, template_device_screen)
        if max_val > 0.8:
            pyautogui.click(max_loc[0], max_loc[1])  # Example action
            self.transition('MAIN_SCREEN')
        else:
            self.transition('ERROR_POPUP')

    def handle_error_popup(self, screenshot):
        max_val, max_loc = match_template(screenshot, template_error_popup)
        if max_val > 0.8:
            pyautogui.click(max_loc[0], max_loc[1])  # Example action to close popup
            self.transition('MAIN_SCREEN')
        else:
            print("Error popup not detected, retrying main screen")
            self.transition('MAIN_SCREEN')

# Function to replay events
def replay_events():
    state_machine = StateMachine()
    while not stop_flag:
        screen = screenshot()
        state_machine.handle_state(screen)
        time.sleep(1)  # Adjust the sleep interval as needed

        # Take screenshot at intervals
        current_time = time.time()
        if current_time >= next_screenshot_time:
            take_screenshot()
            next_screenshot_time = current_time + screenshot_interval

# Start replaying events in a separate thread to allow hotkey to work
replay_thread = threading.Thread(target=replay_events)
replay_thread.start()

# Keep the main thread alive to listen for the 'k' key to stop
keyboard.wait('k')
stop_replay()
replay_thread.join()

print("Replay script has finished or was stopped.")
