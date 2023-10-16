import os
import glob
import re
import pandas as pd

switch = glob.glob('/Users/govardhanrathamsetty/Desktop/ToggleSmell-Chromium/All versions//**/*_switches.cc', recursive=True)
feature = glob.glob('/Users/govardhanrathamsetty/Desktop/ToggleSmell-Chromium/All versions//**/*_features.cc', recursive=True)

cc_files = switch + feature

toggle_list = []

for cc_file in cc_files:
       with open(cc_file, 'r') as file:
                file_contents = file.read()
                toggle_list.append(file_contents)

toggle_list = list(filter(None, toggle_list))
toggle_patterns = [r'const char k.*\]']
found_toggles = []
final_toggle_list = []

for toggles in toggle_list:
    for pattern in toggle_patterns:
        matches = re.findall(pattern,toggles)
        found_toggles.extend(matches)
found_toggles = list(filter(None, found_toggles))

for k_toggles in found_toggles:
    final_toggle_list.extend(re.findall(r'\b[kK]\w*\b',k_toggles))

##Above is toggle extraction from config files.
##Below is mixed toggle code
def mixed(final_toggle_list):
        e=[]
        final=[]
        finall= []
        final_nested_toggle_list=[]

        cc_file3 = glob.glob('/Users/govardhanrathamsetty/Desktop/ToggleSmell-Chromium/All versions/**/chromium 90.0.4390.0/**/*.cc', recursive=True)

        for cc_fil in cc_file3:
            if 'switch' not in cc_fil:
                if 'feature' not in cc_fil:
                    with open(cc_fil, 'rb') as file:  
                        try:
                            content = file.read().decode('utf-8')  
                            e.append(content)
                        except UnicodeDecodeError:
                            pass
                    
        pattern = r'#if .*?#endif'
        empty=[]

        for ee in e:
            matches = re.findall(pattern, ee, re.DOTALL)
            empty.append(matches)

        patt = [emm for emm in empty if emm]

        mixed_list = []
        for mixed in patt:
            for toggle in final_toggle_list:
                matches = re.findall(r'\b[kK]\w*\b', mixed[0])
                if toggle in matches:
                    mixed_list.append(toggle)
        print(len(mixed_list))
    


def dead(final_toggle_list):
        dead_test_files = glob.glob('/Users/govardhanrathamsetty/Desktop/ToggleSmell-Chromium/All versions/**/*.cc', recursive=True)
        dead_list1=[]
        dead_list2= []
        dead_list3=[]
        dead=[]

        for dead in dead_test_files:
            if 'switch' not in dead:
                if 'feature' not in dead:
                    with open(dead, 'rb') as file:  
                        try:
                            content = file.read().decode('utf-8')  
                            dead_list1.append(content)
                        except UnicodeDecodeError:
                            pass

        reg = [r'\(.*\b[kK]\w*\b.*]',r'^const char k.*\]', r'^k.*\]', r'\(\b[kK]\w*\b', r'\(\b[kK]\w*\b.*]' , r'\{\b[kK]\w*\b' , r'\{\b[kK]\w*\b.*]',r'\::k.*',r'\:Feature k.*']

        for dead in dead_list1:
            for r in reg:
                matches = re.findall(r, dead)
                dead_list2.extend(matches)

        dead_list= [re.findall(r'\b[kK]\w*\b', i) for i in dead_list2]

        dead_list = [j for i in dead_list for j in i]

        for i in list(set(dead_list)):
            if i not in list(set(final_toggle_list)):
                dead_list3.append(i)

        print((len(list(set(dead_list))),len(list(set(dead_list3)))))


#mixed(final_toggle_list)
dead(final_toggle_list)
