import os
import glob
import re
import pandas as pd

ch_version = '90.0.4390.0'
#system_root = '/home/taj/Documents/ArchPrediction/ProcessedVersions'
system_root = '/Users/govardhanrathamsetty/Desktop/ToggleSmell-Chromium/All versions/comp_ver'

def nested_toggle(): 
    all_cc_files = glob.glob(f'{system_root}/chromium {ch_version}/**/*.cc', recursive=True)
    file_contents = []
    for cc_file in all_cc_files:
            if 'switch' not in cc_file:
                    if 'feature' not in cc_file:
                        with open(cc_file, 'rb') as file:  
                            try:
                                content = file.read().decode('utf-8')  
                                file_contents.append(content)
                            except UnicodeDecodeError:
                                pass
    file_contents = list(filter(None, file_contents))
    
    for codes in file_contents:
        condensedCode = ''.join(codes).replace(' ', '').replace('\n', ' ')

        regx = [r'if\s*\(.*?\}', r'else\s*\(.*?\}', r'elseif\s*\(.*?\}']

        statementsList = []

        for regg in regx:
            statementsList.append(re.findall(regg, condensedCode))
    
        innerScopeCount = {}

        for statements in statementsList:
            for s in statements:
                total_condition_count = len(re.findall(r'\b(if|else|elseif)\b', s))
                innerScopeCount[s] = total_condition_count
    regs = []
    regMatches = []
    for key, value in innerScopeCount.items():
        reg = re.compile(re.escape(key) + r'.*?\}'*(value))
        regs.append(reg)
    for xx in regs:
        matches = re.findall(xx, condensedCode)
        regMatches.append(matches)

    codeLines = []
    for match in regMatches[0]:
        codeLines.append(match.split(' '))

    nested_toggles = []
    for nested_toggle in codeLines[0]:
        nested_toggles.extend(re.findall(r'\s*k[A-Z].*', nested_toggle))
    print('Following are the Nested Toggles:')
    print('---------------------------------')
    return nested_toggles
    
nested_toggle()