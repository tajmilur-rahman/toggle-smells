import glob
import re
import pandas as pd
from scripts.util import *
from FeatureFlag import *
# system_root = '/Users/govardhanrathamsetty/Desktop/ToggleSmell-Chromium/All versions/comp_ver'
# system_root = '/home/taj/Documents/ArchPrediction/ProcessedVersions'


# components_df = pd.read_csv('/Users/govardhanrathamsetty/Downloads/components.csv')
# toggle_path_df = pd.read_csv('/Users/govardhanrathamsetty/Downloads/1000_comp_matching.csv')
all_cc_files = glob.glob(f'{system_root}/chromium/**/*.cc', recursive=True)

def get_toggles(config_files, toggle_patterns):
    toggle_list = []

    for conf_file in config_files:
        with open(conf_file, 'r', encoding='UTF-8') as file:
            file_content = file.read()
            toggle_list.append(file_content)
            file.close()

    toggle_list = list(filter(None, toggle_list))
    found_toggles = []
    toggles = []

    for toggle in toggle_list:
        for pattern in toggle_patterns:
            matches = re.findall(pattern, toggle)
            found_toggles.extend(matches)
    found_toggles = list(filter(None, found_toggles))

    # for k_toggles in found_toggles:
    #     toggles.extend(re.findall(r'\b[k]\w*\b', k_toggles))
    toggles = found_toggles
    return toggles


# this should be feature flagged lol
def get_toggles_new(config_files, toggle_patterns):
    found_toggles = []

    for conf_file in config_files:
        with open(conf_file, 'r', encoding='UTF-8') as file:
            file_content = file.read()
            for pattern in toggle_patterns:
                matches = re.findall(pattern, file_content)
                for match in matches:
                    if match is None:
                        continue
                    found_toggles.append(FoundToggle(match, conf_file))

            file.close()


    found_toggles = list(filter(None, found_toggles))

    # for k_toggles in found_toggles:
    #     toggles.extend(re.findall(r'\b[k]\w*\b', k_toggles))
    toggles = found_toggles
    return toggles
def extract_dead_toggles():
    toggles = get_toggles()
    return find_dead(toggles)


def extract_mixed_toggles(toggles, regex_pattern, file_extension):
    return find_toggle(regex_pattern, toggles, file_extension)


def extract_enum_toggles(toggles, regex_pattern, file_extension):
    return find_toggle(regex_pattern, toggles, file_extension)

def regrex_playground():
    s = '''
    bool SubprocessNeedsResourceBundle(const std::string& process_type) {
      return
    #if BUILDFLAG(IS_LINUX) || BUILDFLAG(IS_CHROMEOS)
          // The zygote process opens the resources for the renderers.
          process_type == switches::kZygoteProcess ||
    #endif
    #if BUILDFLAG(IS_MAC)
      // Mac needs them too for scrollbar related images and for sandbox
      // profiles.
    #if BUILDFLAG(ENABLE_NACL)
          process_type == switches::kNaClLoaderProcess ||
    #endif
          process_type == switches::kGpuProcess ||
    #endif
          process_type == switches::kPpapiPluginProcess ||
          process_type == switches::kRendererProcess ||
          process_type == switches::kUtilityProcess;
    }

'''

    cpp_mixed_regex = [r'#if.*?\b(k\w+)\b.*?\b(switches::\1)\b.*?#endif']
    print(s)
    for r in cpp_mixed_regex:
        matches = re.findall(r, s, re.DOTALL)
        print(matches)
        print(len(matches))
        for match in matches:
            print(match)


def find_toggle(regexp, toggles, system_root, project_name, file_extension):
    mixed_toggles = []
    all_files = glob.glob(f'{system_root}/{project_name}/**/**.{file_extension}', recursive=True)

    for f in all_files:
        with open(f, 'rb') as file:
            content = repr(file.read().decode('utf-8'))
            for t in toggles:
                try:
                    matches = re.findall(regexp%t, content)
                    if len(matches) > 0:
                        mixed_toggles.append(FoundToggle(t, f, "mixed"))
                        toggles.remove(t)
                        print("found mixed", t)
                        break
                except UnicodeDecodeError:
                    pass
            file.close()

    print(mixed_toggles)
    return mixed_toggles

def find_dead(toggles_list_form_config):  # check with 45th version, no dead toggles found...
    all_cc_files = glob.glob(f'{system_root}/chromium/**/*.cc', recursive=True)

    container1 = []
    container2 = []
    container3 = []

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
    print(dt_list)
    # TODO:Need to get back to this line because the cut-off threshold of 10 is not fully determined
    dt_list = [j for i in dt_list for j in i if len(j) > 10]

    for dt in list(set(dt_list)):
        if len(dt) > 10 and dt not in list(set(toggles_list_form_config)):
            container3.append(dt)

    print((len(list(set(dt_list))), len(list(set(container3)))))  # 3151 off 3454 toggles were seen in .cc files
    print(list(set(container3)))

def extract_nested_toggles():
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
        reg = re.compile(re.escape(key) + r'.*?\}' * (value))
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

    return nested_toggles


# Remove those rows with Component == None
def extract_spread_toggles(toggle_path_df, components_df):
    path_items = []
    tog_map = []
    path_tog_match = []

    for path in toggle_path_df.file_path:
        parts = path.split('/')

        cmpts = parts[8:]

        path_items.append(cmpts)

    path_slicing = []

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
# extract_dead_toggles()
# print(extract_nested_toggles())
# arg1 = (toggle_path_df, components_df)
# extract_mixed_toggles()
# with concurrent.futures.ThreadPoolExecutor() as executor:
#     # Submit tasks
#     # future1 = executor.submit(extract_spread_toggles, *arg1)
#     future2 = executor.submit(extract_dead_toggles)
#     future3 = executor.submit(extract_nested_toggles)
#
#     # Wait for tasks to complete
#     # concurrent.futures.wait([future1, future2, future3])
#     concurrent.futures.wait([future2, future3])
