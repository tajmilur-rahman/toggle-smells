# Toggle Smell Detector

Feature toggle is an worst type of technical debt. There are unknown number of toggle usage patterns created by developers in different source code since there is no standard usage patterns. 
We identified six usage patterns in Google Chromium in a preliminary study. Although, we are not certain yet which toggle usage patterns are to be called as toggle smells, this project is offering a tool to detect toggle usage patterns in different source code. 

Following are the usage patterns our tool can detect as of now.
* Dead usage patterns
* Nested usage patterns
* Spread usage patterns
* Mixed usage patterns 
* Enumeration usage patterns
* Combinatorial usage patterns -- Invalid

## INSTALLATION:
1. Clone the repository:
* https://github.com/tajmilur-rahman/toggle-smells.git

2. CD into ts-detector in commandline

3. Use command: python3 tsd.py -p </source/path> -c </config/path> -o </output/path> -t pattern
