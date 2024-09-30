import re
import json
import regex_c as c_patterns
import regex_java as j_patterns
import regex_python as py_patterns
import regex_go as go_patterns
import regex_csharp as csharp_patterns
from collections import defaultdict

from detectors.enum_detector.enum_detector import *
import helper as helper

import spread_detector as sd
import dead_detector as dd
import nested_detector as nd
import mixed_detector as md

language_map = {
    "c++": c_patterns,
    "java": j_patterns,
    "python": py_patterns,
    "go": go_patterns,
    "csharp": csharp_patterns
}


def detect(lang, code_files, t_config_files, t_usage):
    if lang is None:
        raise ValueError("Language is not defined.")

    if code_files is None:
        raise ValueError("A list of code files is required.")

    if t_config_files is None:
        raise ValueError("A list of config files is required.")

    regex_patterns = {"general_pattern": helper.get_general_toggle_var_patterns(lang),
                      "config_pattern": helper.get_toggle_config_patterns(lang)}

    if t_usage == "dead":
        return extract_dead_toggles(lang, code_files, t_config_files, regex_patterns)
    elif t_usage == "spread":
        return extract_spread_toggles(lang, code_files, t_config_files, regex_patterns)
    elif t_usage == "nested":
        return extract_nested_toggles(lang, code_files, t_config_files, regex_patterns)
    elif t_usage == "mixed":
        return extract_mixed_toggles(lang, code_files, t_config_files, regex_patterns)
    elif t_usage == "enum_detector":
        return extract_enum_toggles(lang, code_files, t_config_files, regex_patterns)


def extract_dead_toggles(lang, code_files, t_config_files, regex_patterns):
    toggles = get_toggles_from_config_files(t_config_files, regex_patterns)
    code_files_contents = helper.get_code_file_contents(lang, code_files)

    if lang == "python":
        toggles = dd.format_python_toggles(toggles)

    dead_toggles = dd.find_dead_toggles(toggles, code_files, code_files_contents)
    return dd.format_dead_toggles_data(dead_toggles)


def extract_nested_toggles(lang, code_files, t_config_files, regex_patterns):
    nested_toggles = defaultdict(list)
    code_files_contents = helper.get_code_file_contents(lang, code_files)
    nested_patterns = helper.get_nested_toggle_patterns(lang)

    nd.process_code_files(lang, code_files, code_files_contents, nested_patterns, nested_toggles, regex_patterns)

    nested_toggles = nd.clean_nested_toggles(nested_toggles)

    return nd.format_nested_toggles_data(nested_toggles)


def extract_spread_toggles(lang, code_files, t_config_files, regex_patterns):
    toggles = get_toggles_from_config_files(t_config_files, regex_patterns)
    toggle_lookup = sd.find_toggles_in_code_files(code_files, toggles)
    spread_toggles = sd.filter_spread_toggles(toggle_lookup)

    parent_toggles = sd.find_parent_toggles(spread_toggles, lang)
    spread_toggles_data = sd.format_spread_toggles(parent_toggles)

    return json.dumps(spread_toggles_data, indent=2)


def extract_mixed_toggles(lang, code_files, t_config_files, regex_patterns):
    mixed_toggles = defaultdict(list)
    code_files_contents = helper.get_code_file_contents(lang, code_files)
    mixed_patterns = helper.get_mixed_toggle_var_patterns(lang)

    md.process_code_files(code_files, code_files_contents, mixed_patterns, mixed_toggles)

    return md.format_mixed_toggles_data(mixed_toggles)

def extract_enum_toggles(code_files, t_config_files, lang, regex_patterns):
    # get all toggle names
    # dictionary to store spread toggle data
    toggle_lookup = defaultdict(list)
    # get all toggles from config files as a set
    toggles = set(get_toggles_from_config_files(t_config_files, regex_patterns))

    code_files_contents = helper.get_code_file_contents(lang, code_files)

    # find all enums and check if name in it
    for code_file, file_content in zip(code_files, code_files_contents):
        res = is_enum_member(file_content, toggles, lang)
        for toggle in res:
            toggle_lookup[toggle].append(code_file)

    return json.dumps(toggle_lookup, indent=2)


def get_toggles_from_config_files(config_files, regex_patterns):
    toggle_list = []
    for conf_file in config_files:
        with open(conf_file, 'r') as file:
            file_content = file.read()
            toggle_list.append(file_content)

    toggle_list = list(filter(None, toggle_list))
    toggle_patterns = regex_patterns['config_pattern']

    toggles = []
    for toggle in toggle_list:
        for pattern in toggle_patterns:
            matches = re.findall(pattern, toggle)
            toggles.extend(matches)

    return list(set(filter(None, toggles)))