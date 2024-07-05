# AutonomousBuildingOperator
AutonomousBuildingOperator is a concept idea project aimed at creating an AI-driven autonomous building operator. Leveraging Generative AI, this system monitors and controls building automation systems (BAS) to optimize comfort, energy efficiency, and operational efficiency.


## TODO
Test on HVAC control system in recording mouse movements to click through graphics like a human building operator would do. Replay clicking through graphics and take screenshots. TODO make Optical Character Recognition (OCR) scripts with `tesseract` to gather data from BAS GUI screenshots and feed into LLM. Experiment with AI being able to override and optimize HVAC. TODO think about how future building user can provide feedback to LLM like a chat bot or something where users of the building can submit temperature control complaint to AI system. 

## Install Python packages
`pip install pillow pyautogui pynput`

Test Python files:
1. Recording Mouse Movements and Clicks 
2. Replaying Mouse Movements and Clicks
3. Combining with Screenshot Capture

## Potential Research Scope and Objectives
This interdisciplinary study aims to investigate how building operators interact with control systems and explore the potential of AI to mimic and enhance these interactions for improved facilities management. By combining insights from psychology, AI, and facilities management, the research will analyze cognitive processes, decision-making strategies, and user interactions through qualitative methods such as interviews, observations, and surveys, as well as quantitative data collection and performance metrics. The study will implement and test an AI system using GUI interactions and OCR, comparing its effectiveness against traditional methods. Performance evaluation, operator feedback, and cost-benefit analysis will be conducted to assess the impact of AI on operational efficiency, energy savings, and occupant comfort, with findings documented in academic publications and presentations.

## intelligent_screen_captures.py 
This is some ideas to try in navigating the BAS like a human building operator.

* **Ensure Data Directory**: The script ensures that the data directory exists.
* **Load Templates**: Templates for different screens and error popups are loaded using OpenCV.
* **stop_flag**: A flag to indicate whether the replay should stop.
* **stop_replay Function**: Sets the stop_flag to True and prints a message.
* **Keyboard Listener**: Uses keyboard.add_hotkey('k', stop_replay) to listen for the 'k' key and stop the replay.
* **take_screenshot Function**: Takes a screenshot and saves it in the data directory.
* **screenshot Function**: Captures the current screen using ImageGrab.
* **match_template Function**: Matches a template in the current screen using OpenCV.
* **StateMachine Class**: Manages different states of the BAS control system interface.
* **handle_state Function**: Handles transitions between different states.
* **replay_events Function**: Contains the event replay logic wrapped in an infinite loop to continuously replay the events until stop_flag is set to True.
* **Start Replay in Separate Thread**: The replay_events function is started in a separate thread to allow the main thread to listen for the 'k' key to stop the replay.

This script continuously navigates the BAS interface, takes screenshots at specified intervals, and handles errors and data delays intelligently using a state machine and image recognition. The replay can be stopped at any time by pressing the `k` key.

```bash
AutonomousBuildingOperator/
│
├── intelligent_screen_captures.py 
└── templates/
    ├── main_screen.png
    ├── device_screen.png
    └── error_popup.png
```
Steps to Prepare and Use the Template Images:
1. Capture Screenshots:
* Manually navigate to the different screens (main screen, device screen, error popup) in your BAS.
* Capture screenshots of these screens using a tool like Snipping Tool, Print Screen, or any other screen capture tool.
* Save these screenshots as `main_screen.png`, `device_screen.png`, and `error_popup.png`.

2. Place Screenshots in the Templates Directory:
* Create a folder named templates in the same directory as your script.
* Move the captured screenshots to the templates folder.

3. Run the Script:
* Ensure that the paths in the script match the location of your templates.
* Run the script, and it will use these templates to identify and interact with the different parts of the BAS interface.

## License
MIT License

Copyright (c) 2024 Ben Bartling

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

ADDITIONAL CYBERSECURITY NOTICE: Users are encouraged to apply the highest level of cybersecurity, OT, IoT, and IT measures when using this software. The authors and copyright holders disclaim any liability for cybersecurity breaches, mechanical equipment damage, financial damage, or loss of life arising from the use of the Software. Users assume full responsibility for ensuring the secure deployment and operation of the Software in their environments.