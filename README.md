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

## License
MIT License

Copyright (c) 2024 Ben Bartling

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

ADDITIONAL CYBERSECURITY NOTICE: Users are encouraged to apply the highest level of cybersecurity, OT, IoT, and IT measures when using this software. The authors and copyright holders disclaim any liability for cybersecurity breaches, mechanical equipment damage, financial damage, or loss of life arising from the use of the Software. Users assume full responsibility for ensuring the secure deployment and operation of the Software in their environments.