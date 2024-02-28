import glob
import re
from scripts.all_toggle_files import *
from scripts.util import *

project_name = 'cadence'
configFile = glob.glob(f'{system_root}/{project_name}/**/constants.go', recursive=True)
allFiles = glob.glob(f'{system_root}/{project_name}/**/**.go', recursive=True)
toggle_pattern = [r'\n*(Enable.*): DynamicBool{']

toggles = get_toggles_new(configFile, toggle_pattern)

def deadToggles(t: list):
    togglesDead = t
    dead_pattern = [r'GetBoolProperty.*%s', r'%s()']
    for file in allFiles:
        if 'constants' not in file:
            with open(file, 'rb') as f:
                try:
                    content = f.read().decode('utf-8')
                    for toggle in togglesDead:
                        if toggle.fname == file:
                            continue
                        pList = allRegExpOfToggles(dead_pattern, toggle.name)
                        for pattern in pList:
                            m = re.findall(pattern, content)
                            if len(m) > 0:
                                togglesDead.remove(toggle)
                                break

                except UnicodeDecodeError:
                    pass

    return togglesDead

t = deadToggles(toggles)
for i in t:
    print(i.name)