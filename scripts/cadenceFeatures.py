import glob
import re
from scripts.all_toggle_files import *
from scripts.util import *

project_name = 'cadence'
configFile = glob.glob(f'{system_root}/{project_name}/**/constants.go', recursive=True)
toggle_pattern = [r'\s*enable[A-Z].*']

toggles = get_toggles(configFile, toggle_pattern)
print(configFile)

print(toggles)
print(len(toggles))

