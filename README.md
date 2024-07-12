# AutonomousBuildingOperator
AutonomousBuildingOperator is a concept idea project aimed at creating an AI-driven autonomous building operator. Leveraging Generative AI, this system monitors and controls building automation systems (BAS) to optimize comfort, energy efficiency, and operational efficiency.


## Goals
1. Gather data with continous screenshotting BAS which would mimic how human building operator would continously look at HVAC controls graphics to monitor system
2. Make use of the data via OCR scripts of obtaining text data from screenshots and saving text data to file.
3. Use data science practices in NLTK world to make sense of the data in the form of noting how the building operated all night long, when did equipment startup in the morning, were there hot or cold zones, is the AHU and central plant equipment running okay, what were the outdoor air temperature conditions like?
4. Ask LLM to summarize all text data and comment if it notices any faults in the HVAC system. Make into a chat feature for a human to chat with the data and LLM in asking how the building has been operating where LLM would respond as if an RCx mechanical engineer for existing building studies.

## Install Python packages
`pip install nltk pillow pynput selenium`


## License
MIT License

Copyright (c) 2024 Ben Bartling

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

ADDITIONAL CYBERSECURITY NOTICE: Users are encouraged to apply the highest level of cybersecurity, OT, IoT, and IT measures when using this software. The authors and copyright holders disclaim any liability for cybersecurity breaches, mechanical equipment damage, financial damage, or loss of life arising from the use of the Software. Users assume full responsibility for ensuring the secure deployment and operation of the Software in their environments.