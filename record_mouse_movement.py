from pynput import mouse
import time

events = []

def on_move(x, y):
    events.append(('move', x, y, time.time()))

def on_click(x, y, button, pressed):
    if pressed:
        events.append(('click', x, y, button, time.time()))

def on_scroll(x, y, dx, dy):
    events.append(('scroll', x, y, dx, dy, time.time()))

# Collect events until released
with mouse.Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll) as listener:
    listener.join()

# Save events to a file
import json
with open('mouse_events.json', 'w') as f:
    json.dump(events, f)
