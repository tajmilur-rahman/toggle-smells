import re
import TogglePatterns as patterns


def detect(code_files, t_config_files, t_usage, lang):
    if t_usage == "dead":
        return extract_dead_toggles(code_files, t_config_files, lang)
    elif t_usage == "spread":
        return extract_spread_toggles(code_files, t_config_files, lang)
    elif t_usage == "nested":
        return extract_nested_toggles(code_files, t_config_files, lang)


def extract_dead_toggles(code_files, t_config_files, lang):
    toggle_list = []

    for conf_file in t_config_files:
        with open(conf_file, 'r') as file:
            file_content = file.read()
            toggle_list.append(file_content)

    toggles = []

    toggle_list = list(filter(None, toggle_list))
    toggle_patterns = list(patterns.toggle_patterns.values())

    for toggle in toggle_list:
        for pattern in toggle_patterns:
            matches = re.findall(pattern, toggle)
            toggles.extend(matches)

    toggles = list(set(filter(None, toggles)))
    return find_dead(code_files, toggles)


def find_dead(code_files, toggles):
    container1 = []
    for cc_file in code_files:
        if 'switch' not in cc_file: # and 'feature' not in cc_file:
            with open(cc_file, 'rb') as file:
                try:
                    content = file.read().decode('utf-8')
                    container1.append(content)
                except UnicodeDecodeError:
                    pass

    potential_toggle_vars = []
    general_toggle_var_patterns = list(patterns.general_toggle_var_patterns.values())

    for file_content in container1:
        for pattern in general_toggle_var_patterns:
            matches = re.findall(pattern, file_content)
            potential_toggle_vars.extend(matches)

    # TODO: Need to get back to this line because the cut-off threshold of 10 is not fully determined
    # In Google Chrome a toggle variable is at least 10 char long. We will remove all others assuming those are not
    # toggle variables
    potential_toggle_vars = list(set([j for j in potential_toggle_vars if len(j) > 10]))

    dead_toggles = []
    for dt in potential_toggle_vars:
        if dt not in toggles:
            dead_toggles.append(dt)

    return list(set(dead_toggles))

def extract_spread_toggles(code_files, t_config_files, lang):
    return []

def extract_nested_toggles(code_files, t_config_files, lang):
    return []