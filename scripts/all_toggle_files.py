import os
import glob
import re
import pandas as pd
import threading
import time
import concurrent.futures


system_root = '/Users/govardhanrathamsetty/Desktop/ToggleSmell-Chromium/All versions/comp_ver'
#system_root = '/home/taj/Documents/ArchPrediction/ProcessedVersions'
ch_version = '80.0.3946.0'
components_df = pd.read_csv('/Users/govardhanrathamsetty/Downloads/components.csv')
toggle_path_df = pd.read_csv('/Users/govardhanrathamsetty/Downloads/1000_comp_matching.csv')

def extract_dead_toggles():
    switch = glob.glob(f'{system_root}/chromium {ch_version}/**/*_switches.cc', recursive=True)
    feature = glob.glob(f'{system_root}/chromium {ch_version}/**/*.cc', recursive=True)

    config_files = switch + feature

    toggle_list = []

    for conf_file in config_files:
           with open(conf_file, 'r') as file:
                    file_content = file.read()
                    toggle_list.append(file_content)

    toggle_list = list(filter(None, toggle_list))
    toggle_patterns = [r'const char k[A-Z].*', r'\::Feature k[A-Z].*', r'\s*k[A-Z].*']
    found_toggles = []
    toggles = []

    for toggle in toggle_list:
        for pattern in toggle_patterns:
            matches = re.findall(pattern, toggle)
            found_toggles.extend(matches)
    found_toggles = list(filter(None, found_toggles))

    for k_toggles in found_toggles:
        toggles.extend(re.findall(r'\b[k]\w*\b',k_toggles))

    return find_dead(toggles)


def find_dead(toggles_list_form_config):   #check with 45th version, no dead toggles found...
            all_cc_files = glob.glob(f'{system_root}/chromium {ch_version}/**/*.cc', recursive=True)
            
            container1=[]
            container2= []
            container3=[]
            container4=[]

            for cc_file in all_cc_files:
                if 'switch' not in cc_file:
                    if 'feature' not in cc_file:
                        with open(cc_file, 'rb') as file:  
                            try:
                                content = file.read().decode('utf-8')  
                                container1.append(content)
                            except UnicodeDecodeError:
                                pass
    
            reg = [r'switches\::k[A-Z].*?\)', r'\s*if\s*\(k[A-Z].*\)', r'\s*\(k[A-Z]', r'\::k[A-Z].*']

            for file_content in container1:
                for r in reg:
                    matches = re.findall(r, file_content)
                    container2.extend(matches)

            dt_list = [re.findall(r'\b[k]\w*\b', line) for line in container2]

            #TODo:Need to get back to this line because the cut-off threshold of 10 is not fully determined
            dt_list = [j for i in dt_list for j in i if len(j) > 10]

            for dt in list(set(dt_list)):
                if len(dt) > 10 and dt not in list(set(toggles_list_form_config)):
                    container3.append(dt)

            print( (len(list(set(dt_list))), len(list(set(container3)))) )  #3151 off 3454 toggles were seen in .cc files
            print( list(set(container3)) )


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

#Remove those rows with Component == None
def spread_toggle(toggle_path_df,components_df):
    path_items=[]
    tog_map=[]
    path_tog_match =[]

    for path in toggle_path_df.file_path:
        
        parts = path.split('/')

        cmpts = parts[8:]
        
        path_items.append(cmpts)
        
    path_slicing=[]

    for columns, content in toggle_path_df.iteritems():
        if columns == 'file_path':
            parts = content.str.split('/')
            toggle_path_df['cmpts'] = parts.apply(lambda path_slicing: path_slicing[8:11])
    toggle_path_df['component_matched'] = None


    for i, row1 in toggle_path_df.iterrows():
        for _, row2 in components_df.iterrows():
            for value in row1['cmpts']:
                if value in row2['name']:           
                    toggle_path_df.at[i, 'component_matched'] = row2['name']
                break
                
    toggle_path_df = toggle_path_df[toggle_path_df['component_matched'].notna()]
    new_comp=components_df.rename(columns={'name': 'component_matched'})
    new_comp = new_comp.drop('source', axis=1)
    spread = pd.concat([group for _, group in toggle_path_df.groupby('toggle_name')])
    spread = spread.merge(new_comp, on='component_matched')
    spread_df = spread.iloc[:, [0, 3, -2, -1]].groupby(['toggle_name', 'component_matched', 'version']).mean().head(20)
    print('Spread Toggle Table:')
    print('--------------------')
    print('--------------------')
    return spread_df


#print(spread_toggle(toggle_path_df, components_df))

#print(extract_dead_toggles())

#print(nested_toggle())

arg1 = (toggle_path_df, components_df)

with concurrent.futures.ThreadPoolExecutor() as executor:
    # Submit tasks
    future1 = executor.submit(spread_toggle, *arg1)
    future2 = executor.submit(extract_dead_toggles)
    future3 = executor.submit(nested_toggle)

    # Wait for tasks to complete
    concurrent.futures.wait([future1, future2, future3])