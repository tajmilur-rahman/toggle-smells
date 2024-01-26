import os
import glob
import re
import pandas as pd

def find_and_list_toggles(directory):
    switch = glob.glob(os.path.join(directory, '**/*_switches.cc'), recursive=True)
    feature = glob.glob(os.path.join(directory, '**/*_features.cc'), recursive=True)

    cc_files = switch + feature

    toggle_list = []
    found_toggles = []
    final_toggle_list = []

    for cc_file in cc_files:
        with open(cc_file, 'r') as file:
            file_contents = file.read()
            toggle_list.append(file_contents)
    toggle_list = list(filter(None, toggle_list))

    toggle_patterns = [
        r'^const char k.*\]',
        r'^k.*\]',
        r'\(\b[kK]\w*\b',
        r'\(\b[kK]\w*\b.*]',
        r'\{\b[kK]\w*\b',
        r'\{\b[kK]\w*\b.*]',
        r'\::k.*',
        r'\:Feature k.*'
    ]

    for toggles in toggle_list:
        for pattern in toggle_patterns:
            matches = re.findall(pattern, toggles)
            found_toggles.extend(matches)
    found_toggles = list(filter(None, found_toggles))

    for k_toggles in found_toggles:
        final_toggle_list.extend(re.findall(r'\b[kK]\w*\b', k_toggles))

    Toggle_df = pd.DataFrame(final_toggle_list, columns={'Toggles'})
    return Toggle_df

# Example usage:
directory_path = '/Users/govardhanrathamsetty/Desktop/ToggleSmell-Chromium/All versions/'
result_df = find_and_list_toggles(directory_path)
print(result_df)
