from pynput import mouse, keyboard
import time
import json
import threading

events = []
recording = False
listener_thread = None

def on_move(x, y):
    if recording:
        events.append(('move', x, y, time.time()))

def on_click(x, y, button, pressed):
    if recording and pressed:
        events.append(('click', x, y, str(button), time.time()))

def on_scroll(x, y, dx, dy):
    if recording:
        events.append(('scroll', x, y, dx, dy, time.time()))

def save_events():
    with open('mouse_events.json', 'w') as f:
        json.dump(events, f)
    print("Mouse events saved to mouse_events.json")

def start_recording():
    global recording, listener_thread
    recording = True
    if not listener_thread:
        listener_thread = threading.Thread(target=mouse_listener)
        listener_thread.start()
    print("Recording started")

def stop_recording():
    global recording
    recording = False
    save_events()
    print("Recording stopped and events saved")

def mouse_listener():
    with mouse.Listener(
            on_move=on_move,
            on_click=on_click,
            on_scroll=on_scroll) as listener:
        listener.join()

def on_press(key):
    try:
        if key.char == 's':  # Press 's' to start recording
            start_recording()
        elif key.char == 'e':  # Press 'e' to stop recording
            stop_recording()
    except AttributeError:
        pass

def on_release(key):
    if key == keyboard.Key.esc:  # Press 'esc' to exit
        if recording:
            stop_recording()
        return False

# Start keyboard listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as k_listener:
    k_listener.join()
