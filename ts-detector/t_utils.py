import re
import os
import regex_c as c_patterns
import regex_java as j_patterns
import regex_python as py_patterns
import regex_go as go_patterns
from collections import defaultdict

language_map = {
    "c++": c_patterns,
    "java": j_patterns,
    "python": py_patterns,
    "go": go_patterns
}


def detect(lang, code_files, t_config_files, t_usage):
    if lang is None:
        raise ValueError("Language is not defined.")

    if code_files is None:
        raise ValueError("A list of code files is required.")

    if t_config_files is None:
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
    # get all toggles from config files
    toggles = get_toggles_from_config_files(lang, t_config_files)
    # get all code file contents in a list
    code_files_contents = get_code_file_contents(lang, code_files)
    # obtain general toggle usage pattern
    general_toggle_var_patterns = get_general_toggle_var_patterns(lang)

    potential_toggle_vars = []
    for file_content in code_files_contents:
        for pattern in general_toggle_var_patterns:
            matches = re.findall(pattern, file_content)
            potential_toggle_vars.extend(matches)

    # TODO: Need to get back to this line because the cut-off threshold of 10 is not fully determined
    min_toggle_var_length = 10

    potential_toggle_vars = [var for var in potential_toggle_vars if len(var) > min_toggle_var_length]
    # filter dead toggles
    dead_toggles = list(set(potential_toggle_vars) - set(toggles))

    return dead_toggles


def extract_spread_toggles(lang, code_files, t_config_files):
    # dictionary to store toggle variables counts
    toggle_lookup = defaultdict(int)
    # get all toggles from config files as a set
    toggles = set(get_toggles_from_config_files(lang, t_config_files))

    # walk through each directory
    for code_file in code_files:
        with open(code_file, 'rb') as file:
            try:
                # read each file content
                content = file.read().decode('utf-8')
                # check for toggle occurrences
                for toggle in toggles:
                    if toggle in content:
                        # increment toggle count
                        toggle_lookup[toggle] += 1
            except UnicodeDecodeError:
                pass

    # filter toggles used in multiple directories
    spread_toggles = {toggle: count for toggle, count in toggle_lookup.items() if count > 1}

    return spread_toggles


def extract_nested_toggles(lang, code_files, t_config_files):
    nested_toggles = []
    # get all code file contents in a list
    code_files_contents = get_code_file_contents(lang, code_files)
    # obtain nested toggle usage pattern
    nested_patterns = get_nested_toggle_patterns(lang)

    for content in code_files_contents:
        for pattern in nested_patterns:
            # check for nested occurrences in file content
            matches = re.findall(pattern, content)
            for match in matches:
                # split the matched code into lines
                code_lines = match.split('\n')
                for line in code_lines:
                    # extract nested toggle variable from each line
                    nested_toggles.extend(re.findall(get_whitespace_patterns(lang), line))

    return nested_toggles


def extract_mixed_toggles(lang, code_files, t_config_files):
    toggles = get_toggles_from_config_files(lang, t_config_files)

    mixed_toggle_var_patterns = get_mixed_toggle_var_patterns(lang)

    mixed_toggles = []
    for f in code_files:
        with open(f, 'rb') as file:
            content = repr(file.read().decode('utf-8'))
            for t in toggles:
                try:
                    for pattern in mixed_toggle_var_patterns:
                        matches = re.findall(pattern % t, content)
                        if len(matches) > 0:
                            mixed_toggles.append(t)

                            toggles.remove(t)
                            break
                except UnicodeDecodeError:
                    pass
            file.close()

    return mixed_toggles


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


def get_condition_count_patterns(lang):
    return language_map[lang.lower()].general_patterns['condition_count']


def get_char_seq_patterns(lang):
    return language_map[lang.lower()].general_patterns['char_seq']


def get_whitespace_patterns(lang):
    return language_map[lang.lower()].general_patterns['whitespace']


def get_toggle_config_patterns(lang):
    return list(language_map[lang.lower()].toggle_config_patterns.values())


def get_general_toggle_var_patterns(lang):
    return list(language_map[lang.lower()].general_toggle_var_patterns.values())


def get_nested_toggle_patterns(lang):
    return list(language_map[lang.lower()].nested_toggle_patterns.values())


def get_mixed_toggle_var_patterns(lang):
    return list(language_map[lang.lower()].mixed_toggle_patterns.values())


def get_code_file_contents(lang, code_files):
    code_files_contents = []
    for file in code_files:
        if lang.lower() == "c++":
            if 'switch' not in file and 'feature' not in file:
                with open(file, 'rb') as f:
                    try:
                        content = f.read().decode('utf-8')
                        code_files_contents.append(content)
                    except UnicodeDecodeError:
                        pass
        else:
            with open(file, 'rb') as f:
                try:
                    content = f.read().decode('utf-8')
                    code_files_contents.append(content)
                except UnicodeDecodeError:
                    pass
    return code_files_contents
