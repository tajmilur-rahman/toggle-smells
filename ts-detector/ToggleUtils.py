import re
import TogglePatterns as patterns


def detect(code_files, t_config_files, t_usage, lang):
    print(lang)
    if t_usage == "dead":
        extract_dead_toggles(code_files, t_config_files, lang)
    elif t_usage == "spread":
        extract_spread_toggles(code_files, t_config_files, lang)
    elif t_usage == "nested":
        extract_nested_toggles(code_files, t_config_files, lang)


def extract_dead_toggles(code_files, t_config_files, lang):
    toggle_list = []

    for conf_file in t_config_files:
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

    return find_dead(code_files, toggles)


def find_dead(code_files, toggles):
    container1 = []

    for cc_file in code_files:
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
        if len(dt) > 10 and dt not in list(set(toggles)):
            container3.append(dt)

    print((len(list(set(dt_list))), len(list(set(container3)))))  # 3151 off 3454 toggles were seen in .cc files
    print(list(set(container3)))

def extract_spread_toggles(code_files, t_config_files, lang):
    return []

def extract_nested_toggles(code_files, t_config_files, lang):
    return []