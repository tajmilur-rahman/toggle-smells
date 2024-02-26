import re
import regex_c as c_patterns
import regex_java as j_patterns
import regex_python as py_patterns


def detect(lang, code_files, t_config_files, t_usage):
    if lang is None:
        raise ValueError("Language is not defined.")

    if code_files is None:
        raise ValueError("A list of code files is required.")

    if code_files is None:
        raise ValueError("A list of config files is required.")

    if t_usage == "dead":
        return extract_dead_toggles(lang, code_files, t_config_files)
    elif t_usage == "spread":
        return extract_spread_toggles(lang, code_files, t_config_files)
    elif t_usage == "nested":
        return extract_nested_toggles(lang, code_files, t_config_files)
    elif t_usage == "mixed":
        return extract_mixed_toggles(lang, code_files, t_config_files)
    elif t_usage == "enum":
        return extract_enum_toggles(lang, code_files, t_config_files)


def extract_dead_toggles(lang, code_files, t_config_files):
    toggles = get_toggles_from_config_files(lang, t_config_files)

    code_files_container = []
    for cc_file in code_files:
        if 'switch' not in cc_file:  # and 'feature' not in cc_file:
            with open(cc_file, 'rb') as file:
                try:
                    content = file.read().decode('utf-8')
                    code_files_container.append(content)
                except UnicodeDecodeError:
                    pass

    general_toggle_var_patterns = get_general_toggle_var_patterns(lang)

    potential_toggle_vars = []
    for file_content in code_files_container:
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


def extract_mixed_toggles(code_files, t_config_files, lang):
    return []


def extract_enum_toggles(code_files, t_config_files, lang):
    return []


def get_toggles_from_config_files(lang, config_files):
    toggle_list = []
    for conf_file in config_files:
        with open(conf_file, 'r') as file:
            file_content = file.read()
            toggle_list.append(file_content)

    toggle_list = list(filter(None, toggle_list))
    toggle_patterns = get_toggle_config_patterns(lang)

    toggles = []
    for toggle in toggle_list:
        for pattern in toggle_patterns:
            matches = re.findall(pattern, toggle)
            toggles.extend(matches)

    return list(set(filter(None, toggles)))


def get_toggle_config_patterns(lang):
    toggle_patterns = []
    if lang.lower() == "c++":
        toggle_patterns = list(c_patterns.toggle_config_patterns.values())
    elif lang.lower() == "java":
        toggle_patterns = list(j_patterns.toggle_config_patterns.values())
    elif lang.lower() == "python":
        toggle_patterns = list(py_patterns.toggle_config_patterns.values())
    return toggle_patterns


def get_general_toggle_var_patterns(lang):
    general_toggle_var_patterns = []
    if lang.lower() == "c++":
        general_toggle_var_patterns = list(c_patterns.general_toggle_var_patterns.values())
    elif lang.lower() == "java":
        general_toggle_var_patterns = list(j_patterns.general_toggle_var_patterns.values())
    elif lang.lower() == "python":
        general_toggle_var_patterns = list(py_patterns.general_toggle_var_patterns.values())
    return general_toggle_var_patterns