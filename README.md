# Toggle-Smells

This Repo contains all files that are related to toggle-smells in chromium source code. It contains code files, that can identify smells in other projects as well. So far, we identified 6 toggle-smell usage patterns.
* Nested usage
* Spread usage
* Dead usage
* Mixed usage
* enumeration usage
* combinatorial usage

    This repository so far will contain the logic for 3 off 6 above toggle smells usage patterns (Nested, Spread, Dead).

# 1. Chromium:

1. First step to identify smells in chromium source code is to have the previous release versions of chromium which can be found in this link: https://github.com/chromium/chromium.
    (Note: Switches.cc, Features.cc are called config files and these contain toggle variable declaration)

2. Next, you need to have python installed in your system: It is recommended to install both Visual studios (https://visualstudio.microsoft.com) and Jupiter Notebook (https://jupyter.org/install) for better validation.

3. Open Visual studios and download python extension. Create a new file to identify feature toggles declared in config files.

4. Install the following packages (import os, import glob, import re, import pandas as pd, import numpy as np).


## INSTALLATION:
1. Download the package and do: 
*  pip install setuptools
*  python path/to/setup.py sdist bdist_wheel
*  pip install togglesmell_detector_installer

2. Access the downloaded file using: path/to/togglesmell_detector_installer


### Toggle variable Extraction:
### Dead Toggle Extraction:
### Nested Toggle Extraction:
### Spread Toggle Extraction:
