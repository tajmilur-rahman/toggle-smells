# Toggle Smell Detector

Feature toggle is an worst type of technical debt. There are unknown number of toggle usage patterns created by developers in different source code since there is no standard usage patterns. 
We identified six usage patterns in Google Chromium in a preliminary study. Although, we are not certain yet which toggle usage patterns are to be called as toggle smells, this project is offering a tool to detect toggle usage patterns in different source code. 

Following are the usage patterns our tool can detect as of now.
* Dead usage patterns
* Nested usage patterns -- In progress
* Spread usage patterns -- In progress
* Mixed usage patterns -- In progress
* Enumeration usage patterns -- In progress
* Combinatorial usage patterns -- In progress

## INSTALLATION:
1. Clone the repository:
* https://github.com/tajmilur-rahman/toggle-smells.git

2. CD into ts-detector in commandline

3. Use command:
* python3 tsd.py <language> </source/code/directory/path> <config_file_postfix> <toggle_usage_type>
* Example: python3 tsd.py C++ /Users/user/Documents/Data/chromium/ui/base switches.cc dead
