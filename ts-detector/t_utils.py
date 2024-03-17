import re
import glob

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


def extract_spread_toggles(lang, code_files, t_config_files):
    # find all the toggles
    # find their usages across the project
    # for each toggle, compare its usage with each other,
    # if there >= 2 usages within different root directory,
    # it is a spread
    # golang => check package, OOR => check class, last fallback option => directory

    toggles = get_toggles_from_config_files(lang, t_config_files)

    spread_toggles_check = {}
    spread_toggles = []
    for f in code_files:
        with open(f, 'rb') as file:
            content = repr(file.read().decode('utf-8'))
            for t in toggles:
                try:
                    matches = re.findall(t, content)  # t => toggle name, content => file content
                    parent_pattern = language_map[lang].spread_toggle_patterns['parent_finder']
                    parent = re.findall(parent_pattern % t, content)
                    if len(matches) > 0:
                        for m in matches:

                            if m not in spread_toggles and parent != '':
                                spread_toggles_check[m] = [parent]
                            elif parent != '' and parent not in spread_toggles_check[m]:
                                spread_toggles_check[m].append(parent)

                        continue
                except UnicodeDecodeError:
                    pass
            file.close()
    for t in toggles:
        if t in spread_toggles_check and len(spread_toggles_check[t]) >= 2:
            spread_toggles.append(toggles)
    return spread_toggles


def extract_nested_toggles(lang, code_files, t_config_files):
    nested_toggle_var_patterns = get_nested_toggle_var_patterns(lang)

    if_pattern = nested_toggle_var_patterns['if_condition']
    else_pattern = nested_toggle_var_patterns['else_condition']
    elif_pattern = nested_toggle_var_patterns['elseif_condition']

    regx = [if_pattern, else_pattern, elif_pattern]

    innerScopeCount = {}

    for f in code_files:
        with open(f, 'rb') as file:
            try:
                content = file.read().decode('utf-8')
                condensedCode = ''.join(content).replace(' ', '').replace('\n', ' ')
                statementsList = []
                for regg in regx:
                    statementsList.append(re.findall(regg, condensedCode))

                for statements in statementsList:
                    for s in statements:
                        total_condition_count = len(re.findall(r'\b(if|else|elseif)\b', s))
                        innerScopeCount[s] = total_condition_count
            except UnicodeDecodeError:
                pass

            file.close()

    regs = []
    regMatches = []
    for key, value in innerScopeCount.items():
        reg = re.compile(re.escape(key) + r'.*?\}' * value)
        regs.append(reg)


    for xx in range(10):
        print(regs[xx])
        matches = re.findall(regs[xx], condensedCode)
        regMatches.append(matches)

    print(regMatches)
    codeLines = []
    for match in regMatches[0]:
        codeLines.append(match.split(' '))

    nested_toggles = []
    for nested_toggle in codeLines[0]:
        nested_toggles.extend(re.findall(r'\s*k[A-Z].*', nested_toggle))

    return nested_toggles

    return []


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

def extract_combinatory_toggles(code_files, t_config_files, lang):
    toggle_names = get_toggles_from_config_files(lang, t_config_files)

    for code in code_files:
        # Build regular expression pattern to match toggles within the same conditional statement
        toggle_pattern = '|'.join(toggle_names)
        conditional_pattern = r'\b(?:if|else\s*if)\s*\((?:[^{}]*\b(?:' + toggle_pattern + r')\b[^{}]*,?\s*)+\)\s*{'

        # Find all occurrences of conditional statements containing multiple toggles
        conditional_matches = re.finditer(conditional_pattern, code)

        # Check each conditional statement for combinations of toggles
        combination_detected = False
        for match in conditional_matches:
            conditional_statement = match.group(0)
            combination_found = False
            for toggle in toggle_names:
                if toggle in conditional_statement:
                    for other_toggle in toggle_names:
                        if toggle != other_toggle and other_toggle in conditional_statement:
                            combination_detected = True
                            combination_found = True
                            print(f"Combination detected: {toggle} and {other_toggle}")
                            break
                    if combination_found:
                        break

        if not combination_detected:
            print("No combinatorial toggle pattern detected in the code file.")




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
    return list(language_map[lang.lower()].toggle_config_patterns.values())


def get_general_toggle_var_patterns(lang):
    return list(language_map[lang.lower()].general_toggle_var_patterns.values())


def get_mixed_toggle_var_patterns(lang):
    return list(language_map[lang.lower()].mixed_toggle_patterns.values())

def get_nested_toggle_var_patterns(lang):
    return language_map[lang.lower()].nested_toggle_patterns

# Fits a toggle name into regexes
# regex is [] of patterns
# toggleName string of name of toggle
# e.g. ([r'%s()'], toggle1) => [r'toggle1()']
def getRegexWithToggleName(regex, toggleName):
    return [p % toggleName for p in regex]
