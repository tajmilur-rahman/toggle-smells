import re
import regex_c as c_patterns
import regex_java as j_patterns
import regex_python as py_patterns
import regex_go as go_patterns

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
    # In Google Chrome a toggle variable is at least 10 char long. We will remove all others assuming those are not
    # toggle variables
    potential_toggle_vars = list(set([j for j in potential_toggle_vars if len(j) > 10]))

    dead_toggles = []
    for dt in potential_toggle_vars:
        if dt not in toggles:
            dead_toggles.append(dt)
    return list(set(dead_toggles))


def extract_spread_toggles(lang, code_files, t_config_files):
    # get all toggles from config files
    toggles = get_toggles_from_config_files(lang, t_config_files)

    spread_toggles_check = {}
    spread_toggles = []
    for f in code_files:
        with open(f, 'rb') as file:
            content = repr(file.read().decode('utf-8'))
            for t in toggles:
                try:
                    matches = re.findall(t, content)
                    if len(matches) > 0:
                        for m in matches:
                            if m not in spread_toggles:
                                spread_toggles_check[m] = 1
                            else:
                                spread_toggles_check[m] += 1
                                spread_toggles.append(m)
                        continue
                except UnicodeDecodeError:
                    pass
            file.close()

    return spread_toggles


def extract_nested_toggles(code_files, t_config_files, lang):
    inner_scope_count = {}

    # get all code file contents in a list
    code_files_contents = get_code_file_contents(lang, code_files)

    condensed_code = ''

    for codes in code_files_contents:
        statements_list = []
        condensed_code = ''.join(codes).replace(' ', '').replace('\n', ' ')
        # obtain nested toggle usage pattern
        nested_patterns = get_nested_toggle_patterns(lang)

        for p in nested_patterns:
            statements_list.append(re.findall(p, condensed_code))

        for statements in statements_list:
            for s in statements:
                total_condition_count = len(re.findall(get_condition_count_patterns(lang), s))
                inner_scope_count[s] = total_condition_count

    regs = []
    reg_matches = []

    for key, value in inner_scope_count.items():
        reg = re.compile(re.escape(key) + get_char_seq_patterns(lang) * value)
        regs.append(reg)

    for reg in regs:
        matches = re.findall(reg, condensed_code)
        reg_matches.append(matches)

    code_lines = []
    for match in reg_matches[0]:
        code_lines.append(match.split(' '))

    nested_toggles = []
    for nested_toggle in code_lines[0]:
        nested_toggles.extend(re.findall(get_whitespace_patterns(lang), nested_toggle))

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
