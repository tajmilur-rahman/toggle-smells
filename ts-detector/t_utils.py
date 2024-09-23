import re
import json
import regex_c as c_patterns
import regex_java as j_patterns
import regex_python as py_patterns
import regex_go as go_patterns
import regex_csharp as csharp_patterns
from collections import defaultdict

from enum_detector.enum_detector import *

language_map = {
    "c++": c_patterns,
    "java": j_patterns,
    "python": py_patterns,
    "go": go_patterns,
    "csharp": csharp_patterns
}


def detect(lang, code_files, t_config_files, t_usage, regex_patterns):
    if lang is None:
        raise ValueError("Language is not defined.")

    if code_files is None:
        raise ValueError("A list of code files is required.")

    if t_config_files is None:
        raise ValueError("A list of config files is required.")

    if regex_patterns == {}:
        regex_patterns["general_pattern"] = get_general_toggle_var_patterns(lang)
        regex_patterns["config_pattern"] = get_toggle_config_patterns(lang)

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
    # get all toggles from config files
    toggles = get_toggles_from_config_files(t_config_files, regex_patterns)
    # get all code file contents in a list
    code_files_contents = get_code_file_contents(lang, code_files)

    if lang == "python":
        for j in range(len(toggles)):
            toggles[j] = "\"" + toggles[j] + "\""

    dead_toggles = toggles
    for code_file, file_content in zip(code_files, code_files_contents):
        for toggle in toggles:
            # search for toggle matches
            matches = re.findall(toggle, file_content)
            if len(matches) > 0:
                dead_toggles.remove(toggle)

    # format dead toggles dictionary
    dead_toggles_data = {
        "dead_toggles": dead_toggles,
        "total_count": len(dead_toggles)
    }
    # convert dictionary to JSON object
    dead_toggles_json = json.dumps(dead_toggles_data, indent=2)

    return dead_toggles_json


def extract_nested_toggles(lang, code_files, t_config_files, regex_patterns):
    # dictionary to store nested toggle data
    nested_toggles = defaultdict(list)

    # get all toggles from config files
    toggles = get_toggles_from_config_files(t_config_files, regex_patterns)

    # get all code file contents in a list
    code_files_contents = get_code_file_contents(lang, code_files)
    # obtain nested toggle usage pattern
    nested_patterns = get_nested_toggle_patterns(lang)
    # set to store distinct nested toggle variables
    distinct_toggles = set()

    for code_file, content in zip(code_files, code_files_contents):
        for pattern in nested_patterns:
            # check for nested occurrences in file content
            matches = re.findall(pattern, content)
            for match in matches:
                # split the matched code into lines
                if lang == "python": # python doesn't have {} so we need to take another route
                    code_lines = [match.replace('\n', "")]
                else:
                    code_lines = match.split('\n')
                for line in code_lines:
                    # populate dictionary with nested toggle data
                    for i in regex_patterns["general_pattern"]:
                        nested_toggles[getFileName(lang,code_file)].extend(re.findall(i, line))

    to_del = []
    for k in nested_toggles.keys():
        nested_toggles[k] = list(dict.fromkeys(nested_toggles[k]))
        distinct_toggles.update(nested_toggles[k])
        if len(nested_toggles[k]) == 0:
            to_del.append(k)

    for i in to_del: del nested_toggles[i]

    # format nested toggles dictionary
    nested_toggles_data = {
        "nested_toggles": nested_toggles,
        "total_count_path": len(nested_toggles),
        "total_count_toggles": len(distinct_toggles)
    }
    # convert dictionary to JSON object
    nested_toggles_json = json.dumps(nested_toggles_data, indent=2)
    return nested_toggles_json


def extract_spread_toggles(lang, code_files, t_config_files, regex_patterns):
    # dictionary to store spread toggle data
    toggle_lookup = defaultdict(list)
    # get all toggles from config files as a set
    toggles = set(get_toggles_from_config_files(t_config_files, regex_patterns))
    # walk through each directory
    for code_file in code_files:
        with open(code_file, 'rb') as file:
            try:
                # read each file content
                content = file.read().decode('utf-8')
                # check for toggle occurrences
                for toggle in toggles:
                    if toggle in content:
                        # populate dictionary with spread toggle data
                        toggle_lookup[toggle].append((code_file, content))
            except UnicodeDecodeError:
                pass

    # filter toggles used in multiple directories
    spread_toggles = {toggle: count for toggle, count in toggle_lookup.items() if len(count) > 1}

    toggle_parent_patterns = get_spread_toggle_var_patterns(lang)['parent_finder']

    toggles = defaultdict(list)
    # find its parent
    for toggle, contents in spread_toggles.items():
        parent_list = []
        for content in contents:
            for pattern in toggle_parent_patterns:
                try:
                    p = pattern % toggle
                except:
                    p = pattern

                matches = re.findall(p, content[1])

                for match in matches:
                    if match not in parent_list:
                        parent_list.append((match[0], getFileName(lang, content[0])))

        if len(parent_list) != 0:
            toggles[toggle].extend(parent_list)
            toggles[toggle] = list(dict.fromkeys(toggles[toggle]))

    s_toggles = defaultdict(list)
    for t in toggles.keys():
        if len(toggles[t]) > 1:
            s_toggles[t] = list(dict.fromkeys(toggles[t]))

    # format spread toggles dictionary
    spread_toggles_data = {
        "spread_toggles": s_toggles,
        "total_count": len(s_toggles)
    }
    # convert dictionary to JSON object
    spread_toggles_json = json.dumps(spread_toggles_data, indent=2)

    return spread_toggles_json


def extract_mixed_toggles(lang, code_files, t_config_files, regex_patterns):
    # dictionary to store mixed toggle data
    mixed_toggles = defaultdict(list)
    # get all code file contents in a list
    code_files_contents = get_code_file_contents(lang, code_files)
    # obtain mixed toggle usage pattern
    mixed_patterns = get_mixed_toggle_var_patterns(lang)

    for code_file, content in zip(code_files, code_files_contents):
        for pattern in mixed_patterns:
            # check for mixed occurrences in file content
            matches = re.findall(pattern, content)
            for match in matches:
                # populate dictionary with mixed toggle data
                mixed_toggles[match].append((code_file, matches.count(match)))

    # format mixed toggles dictionary
    mixed_toggles_data = {
        "mixed_toggles": mixed_toggles,
        "total_count": len(mixed_toggles)
    }
    # convert dictionary to JSON object
    mixed_toggles_json = json.dumps(mixed_toggles_data, indent=2)

    return mixed_toggles_json


def extract_enum_toggles(code_files, t_config_files, lang, regex_patterns):
    # get all toggle names
    # dictionary to store spread toggle data
    toggle_lookup = defaultdict(list)
    # get all toggles from config files as a set
    toggles = set(get_toggles_from_config_files(t_config_files, regex_patterns))

    code_files_contents = get_code_file_contents(lang, code_files)

    patterns = get_enum_toggle_var_patterns()
    # find all enums and check if name in it
    for code_file, file_content in zip(code_files, code_files_contents):
        for toggle in toggles:
            # search for toggle matches
            is_enum_member(file_content, toggle, lang)



    return []


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


def get_directive_patterns(lang):
    return language_map[lang.lower()].mixed_toggle_patterns['if_directive']


def get_toggle_config_patterns(lang):
    return list(language_map[lang.lower()].toggle_config_patterns.values())


def get_general_toggle_var_patterns(lang):
    return list(language_map[lang.lower()].general_toggle_var_patterns.values())


def get_nested_toggle_patterns(lang):
    return list(language_map[lang.lower()].nested_toggle_patterns.values())


def get_mixed_toggle_var_patterns(lang):
    return list(language_map[lang.lower()].mixed_toggle_patterns.values())


def get_spread_toggle_var_patterns(lang):
    return language_map[lang.lower()].spread_toggle_patterns


def get_nested_toggle_var_patterns(lang):
    return language_map[lang.lower()].nested_toggle_patterns


def get_enum_toggle_var_patterns(lang):
    return language_map[lang.lower()].enum_toggle_patterns

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


# Fits a toggle name into regexes
# regex is [] of patterns
# toggleName string of name of toggle
# e.g. ([r'%s()'], toggle1) => [r'toggle1()']
def getRegexWithToggleName(regex, toggleName):
    return [p % toggleName for p in regex]


def getFileName(lang, path):
    if(lang == "python"):
        regex = r"[^\/]*\.py"
        return re.findall(regex, path)[0]
    elif(lang == "js"):
        regex = r"[^\/]*\.js"
        return re.findall(regex, path)[0]
    elif(lang == 'java'):
        regex = r"[^\/]*\.java"
        return re.findall(regex, path)[0]
    elif(lang == 'go'):
        regex = r"[^\/]*\.go"
        return re.findall(regex, path)[0]

    return path

