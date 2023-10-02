import os
import glob
import re
import pandas as pd

def process_code_files():
    switch = glob.glob('/Users/govardhanrathamsetty/Desktop/ToggleSmell-Chromium/All versions/**/*_switches.cc', recursive=True)
    feature = glob.glob('/Users/govardhanrathamsetty/Desktop/ToggleSmell-Chromium/All versions/**/*_features.cc', recursive=True)

    cc_files = switch + feature

    path_filecontent={}
    emp_dic = {}
    emp_list, emp_list2, ss, comp_tog_match=[[],[],[],[]]

    for cc_file in cc_files:
        with open(cc_file, 'r') as file:
            file_contents = file.read()
            emp_dic[cc_file] = file_contents
    emp_dic = {key: value for key, value in emp_dic.items() if value is not None and value != ''}
    for i,j in emp_dic.items():
        i = i.split('\n')
        emp_list.append((i, j))

    for i in emp_list:
        i = (i[0][0], i[1])
        emp_list2.append(i)

    for i in emp_list2:
        path_filecontent[i[0]] = i[1]

    reg = [r'^const char k.*\]', r'^k.*\]', r'\(\b[kK]\w*\b', r'\(\b[kK]\w*\b.*]' , r'\{\b[kK]\w*\b' , r'\{\b[kK]\w*\b.*]', r'\::k.*', r'\:Feature k.*']

    for i, j in path_filecontent.items():
        parts = i.split('/')
        file_name = parts[-1]
        version = '/'.join(parts[7:8])
        wrapping_component = '/'.join(parts[9:10])
        component = '/'.join(parts[8:9])
        j = j.split('\n')
        ss.append(j)

        for q in ss:
            for kk in q:
                for regg in reg:
                    matches = re.findall(regg, kk)
                    for mat in matches:
                        matches = re.findall(r'\b[kK]\w*\b',mat)
                        if matches:
                            comp_tog_match.append((i,version, component, wrapping_component, file_name, matches))

    finaldf = pd.DataFrame(comp_tog_match, columns =['Path', 'Version', 'Component', 'Wrappping_Component','File_name', 'Toggle_Matches'])

    return finaldf

# Call the function to process the code files
result_df = process_code_files()
print(result_df)
