import glob
import re
import pandas as pd
import concurrent.futures
import toggle_patterns as patterns

system_root = '/Users/govardhanrathamsetty/Desktop/ToggleSmell-Chromium/All versions/comp_ver'
# system_root = '/home/taj/Documents/ArchPrediction/ProcessedVersions'
ch_version = '80.0.3946.0'
components_df = pd.read_csv('/Users/govardhanrathamsetty/Downloads/components.csv')
toggle_path_df = pd.read_csv('/Users/govardhanrathamsetty/Downloads/1000_comp_matching.csv')


def extract_dead_toggles():
    switch = glob.glob(f'{system_root}/chromium {ch_version}/**/*_switches.cc', recursive=True)
    feature = glob.glob(f'{system_root}/chromium {ch_version}/**/*.cc', recursive=True)

    toggle_list = []
    config_files = switch + feature

    for conf_file in config_files:
        with open(conf_file, 'r') as file:
            file_content = file.read()
            toggle_list.append(file_content)

    toggles = []
    found_toggles = []

    toggle_list = list(filter(None, toggle_list))
    toggle_patterns = list(patterns.toggle_patterns.values())

    for toggle in toggle_list:
        for pattern in toggle_patterns:
            matches = re.findall(pattern, toggle)
            found_toggles.extend(matches)

    found_toggles = list(filter(None, found_toggles))
    for k_toggles in found_toggles:
        toggles.extend(re.findall(patterns.general_patterns['pattern_key'], k_toggles))

    return find_dead(toggles)


:q!
def find_dead(toggles_list_form_config):  # check with 45th version, no dead toggles found...
    all_cc_files = glob.glob(f'{system_root}/chromium {ch_version}/**/*.cc', recursive=True)
    container1 = []

    for cc_file in all_cc_files:
        if 'switch' not in cc_file and 'feature' not in cc_file:
            with open(cc_file, 'rb') as file:
                try:
                    content = file.read().decode('utf-8')
                    container1.append(content)
                except UnicodeDecodeError:
                    pass

    container2 = []
    dead_patterns = list(patterns.dead_toggle_patterns.values())

    for file_content in container1:
        for pattern in dead_patterns:
            matches = re.findall(pattern, file_content)
            container2.extend(matches)

    dt_list = [re.findall(patterns.general_patterns['pattern_key'], line) for line in container2]
    # TODO: Need to get back to this line because the cut-off threshold of 10 is not fully determined
    dt_list = [j for i in dt_list for j in i if len(j) > 10]

    container3 = []
    for dt in list(set(dt_list)):
        if len(dt) > 10 and dt not in list(set(toggles_list_form_config)):
            container3.append(dt)

    print((len(list(set(dt_list))), len(list(set(container3)))))  # 3151 off 3454 toggles were seen in .cc files
    print(list(set(container3)))


def extract_nested_toggles():
    all_cc_files = glob.glob(f'{system_root}/chromium {ch_version}/**/*.cc', recursive=True)
    file_contents = []
    inner_scope_count = {}

    for cc_file in all_cc_files:
        if 'switch' not in cc_file and 'feature' not in cc_file:
            with open(cc_file, 'rb') as file:
                try:
                    content = file.read().decode('utf-8')
                    file_contents.append(content)
                except UnicodeDecodeError:
                    pass

    file_contents = list(filter(None, file_contents))
    condensed_code = ''

    for codes in file_contents:
        statements_list = []
        condensed_code = ''.join(codes).replace(' ', '').replace('\n', ' ')

        nested_patterns = list(patterns.nested_toggle_patterns.values())

        for pattern in nested_patterns:
            statements_list.append(re.findall(pattern, condensed_code))

        for statements in statements_list:
            for statement in statements:
                total_condition_count = len(re.findall(patterns.general_patterns['condition_count'], statement))
                inner_scope_count[statement] = total_condition_count

    regs = []
    reg_matches = []

    for key, value in inner_scope_count.items():
        reg = re.compile(re.escape(key) + patterns.general_patterns['char_seq'] * value)
        regs.append(reg)

    for reg in regs:
        matches = re.findall(reg, condensed_code)
        reg_matches.append(matches)

    code_lines = []
    for match in reg_matches[0]:
        code_lines.append(match.split(' '))

    nested_toggles = []
    for nested_toggle in code_lines[0]:
        nested_toggles.extend(re.findall(patterns.toggle_patterns['whitespace'], nested_toggle))

    print('Following are the Nested Toggles:')
    print('---------------------------------')
    return nested_toggles


# Remove those rows with Component == None
def extract_spread_toggles(toggle_path_df, components_df):
    path_items = []

    for path in toggle_path_df.file_path:
        parts = path.split('/')
        cmpts = parts[8:]
        path_items.append(cmpts)

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

    new_comp = components_df.rename(columns={'name': 'component_matched'})
    new_comp = new_comp.drop('source', axis=1)

    spread = pd.concat([group for _, group in toggle_path_df.groupby('toggle_name')])
    spread = spread.merge(new_comp, on='component_matched')
    spread_df = spread.iloc[:, [0, 3, -2, -1]].groupby(['toggle_name', 'component_matched', 'version']).mean().head(20)

    print('Spread Toggle Table:')
    print('--------------------')
    print('--------------------')
    return spread_df


# print(spread_toggle(toggle_path_df, components_df))

# print(extract_dead_toggles())

# print(extract_nested_toggles())

arg1 = (toggle_path_df, components_df)

with concurrent.futures.ThreadPoolExecutor() as executor:
    # Submit tasks
    future1 = executor.submit(extract_spread_toggles, *arg1)
    future2 = executor.submit(extract_dead_toggles)
    future3 = executor.submit(extract_nested_toggles)

    # Wait for tasks to complete
    concurrent.futures.wait([future1, future2, future3])
