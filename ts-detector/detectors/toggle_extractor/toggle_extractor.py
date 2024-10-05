import re

comment_regexes = {
    'python': r'^\s*#.*$',
    'csharp': r'^\s*//.*$',
    'java': r'^\s*//.*$',
    'golang': r'^\s*//.*$',
    "c++": r'^\s*//.*$',
}

regexes = {
    'python': {
        'declare': r'(?P<toggle>\w+)\s*(?:\:\s*(?P<type>[^\s=]+))?\s*=\s*',
        'capital_identifiers': r'(?P<toggle>[A-Z][A-Z0-9_-]{2,})',
        'dict_keys': r'[{,]\s*(?P<toggle>(?:[\'\"][^\'\"]*[\'\"]|[^:]+?))\s*:',
        'enum_names': r'class\s+(?P<toggle>\w+)\(Enum\):'
    },
    'csharp': {
        'declare': (
            r'(public|protected|private\s+protected|private)\s+(?:static\s+|const\s+|readonly\s+)*(\w+(?:\s*<[^>]+>)?)\s+(?P<toggle>\w+)\s*(?=\s*(=|;|\[))'
        ),
        'capital_identifiers': r'(?P<toggle>[A-Z][A-Z0-9_-]{2,})',
        'dict_keys': r'[{,]\s*(?P<toggle>(?:@"[^"]*"|"[^"]*"|\'[^\']*\'|[^,\s]+?))\s*,',
        'enum_names': r'enum\s+(?P<toggle>\w+)\s*'
    },
    'java': {
        'declare': (
            r'(public|protected|private)\s+'
            r'(?:static\s+|final\s+|volatile\s+|transient\s+)*'
            r'(?P<type>\w+(?:\s*<[^>]+>)?)\s+'
            r'(?P<toggle>\w+)\s*'
            r'(?=\s*(=|;|\[))'
        ),
        'capital_identifiers': r'(?P<toggle>[A-Z][A-Z0-9_-]{2,})',
        'dict_keys': r'\bput\s*\(\s*(?P<toggle>"[^"]*"|\'[^\']*\'|[^,\s]+?)\s*,',
        'enum_names': r'enum\s+(?P<toggle>\w+)\s*'
    },
    'golang': {
        'declare': (
            r'(?:var\s+(?P<toggle>\w+)\s*(?:\s+(?P<type>[^\s=]+))?\s*(?:=\s*.*)?|'
            r'(?P<toggle2>\w+)\s*(?:\s+(?P<type2>[^\s=]+))?\s*:=\s*.*)'
        ),
        'declare2': r'\s+(?P<toggle>\w+)\s* =',
        'capital_identifiers': r'(?P<toggle>[A-Z][A-Z0-9_-]{2,})',
        'dict_keys': r'[{,]\s*(?P<toggle>(?:`[^`]*`|"[^"]*"|\'[^\']*\'|[\w.]+?))\s*:',
        'enum_names': r'type\s+(?P<toggle>\w+)\s+int\s*'
    },
    "c++": {
        'declare': (
            r'(?:(?:const|static|volatile|extern|mutable)\s+)*'
            r'(?P<type>(?:[\w:]+)(?:\s*<[^>;]+>)?'
            r'(?:\s*::\s*[\w:]+)*(?:\s*[\*&])?)\s+'
            r'(?P<toggle>\w+)\s*'
            r'(?=\s*(=|;|\[))'
        ),
        'capital_identifiers': r'(?P<toggle>[A-Z][A-Z0-9_-]{2,})',
        'dict_keys': r'[{,]\s*(?P<toggle>(?:"[^"]*"|\'[^\']*\'|[^,\s]+?))\s*,',
        'toggle_names': r'(Feature)?(Toggle|Flag|Enable|Disable)?\w*::(?P<toggle>\w+),',
        'enum_names': r'enum\s+(?P<toggle>\w+)\s*'
    }
}

language_keywords = {
    'python': ['__', '__main__', 'True', 'False', 'None', 'async', 'await', 'self', '"true"', '"false"', '__name__', '"CRITICAL"', '"ERROR"', '"WARNING"', '"INFO"'],
    'csharp': ['public', 'private', 'protected', 'const', 'static', 'readonly', 'string', 'Dictionary', 'List', 'bool',
               '"true"', '"false"', '"CRITICAL"', '"ERROR"', '"WARNING"', '"INFO"'],
    'java': ['public', 'private', 'protected', 'static', 'final', 'volatile', 'transient', 'String', 'Map', 'List',
             'boolean', '"true"', '"false"', '"CRITICAL"', '"ERROR"', '"WARNING"', '"INFO"'],
    'golang': ['var', 'const', 'func', 'int', 'string', 'bool', 'map', '"true"', '"false"', 'err', 'ok', '"CRITICAL"', '"ERROR"', '"WARNING"', '"INFO"'],
    "c++": ['const', 'static', 'public', 'private', 'protected', 'bool', 'int', 'float', 'double', 'std', '"true"',
            '"false"', '"CRITICAL"', '"ERROR"', '"WARNING"', '"INFO"']
}


def is_pure_number_or_dash_underscore(toggle):
    return bool(re.fullmatch(r'"?\d+([-_\.]\d+)*"?', toggle))


def no_invalid_chars(toggle):
    invalid_chars = ['(', ')', '{', '}', '[', ']', '|', '\\', ';', '<', '>', ' ', '!', '@', 'https://', 'http://',
                     'localhost:']
    for char in invalid_chars:
        if char in toggle:
            return False
    return True


def larger_is_from_toggle(content, var_a, var_b):
    pattern = rf'\b{re.escape(var_a)}\s*=\s*[\s\S]*?{re.escape(var_b)}[\s\S]*?;'
    matches = re.findall(pattern, content)
    return len(matches) > 0


def filter_substrings(toggles, config_file_contents):
    toggles = sorted(toggles, key=len, reverse=True)
    filtered_toggles = []
    for toggle in toggles:
        flag = True
        for larger_toggle in toggles:
            if toggle in larger_toggle and toggle != larger_toggle:
                flag = False
                content = config_file_contents.replace(larger_toggle, "")
                if toggle in content and not larger_is_from_toggle(config_file_contents, larger_toggle, toggle):
                    filtered_toggles.append(toggle)
        if flag:
            filtered_toggles.append(toggle)
    return filtered_toggles


def extract_value_for_toggle(toggle, config_file_contents):
    assignment_pattern = re.compile(rf'{re.escape(toggle)}.*\s*=\s*(.+)\n')
    match = assignment_pattern.search(config_file_contents)

    if match:
        value = match.group(1).strip()
        if value.startswith(("'", '"')) and value.endswith(("'", '"')):
            value = value[1:-1]
        return value

    assignment_pattern = (re.compile(rf'{re.escape(toggle)}.*\s*:\s*(.+)\n'))
    match = assignment_pattern.search(config_file_contents)
    if match:
        value = match.group(1).strip()
        if value.startswith(("'", '"')) and value.endswith(("'", '"')):
            value = value[1:-1]
        return value

    return None


def filter_wrong_values(toggles, config_file_contents):
    dict_or_list_pattern = r'[\{\[\(]'
    ip_address_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    percentage_pattern = r'\b\d+%+'
    url_pattern = r'(https?://[^\s]+)'
    invalid_int_pattern = r'\b(?!0\b|1\b)\d+\b'
    directory_pattern = r'([a-zA-Z]:\\|\/)[^<>:"|?*]+(?:\\|\/)[^<>:"|?*]*'
    language_code_pattern = r'\b[a-z]{2}\b'
    None_pattern = r'None|Null|none|null|undefined'
    function_call_pattern = r'\w+\s*\(.*'


    filtered_toggles = []
    for toggle in toggles:
        value = extract_value_for_toggle(toggle, config_file_contents)
        if value:
            if (not re.search(dict_or_list_pattern, value) and
                    not re.search(ip_address_pattern, value) and
                    not re.search(percentage_pattern, value) and
                    not re.search(url_pattern, value) and
                    not re.search(directory_pattern, value) and
                    not re.search(language_code_pattern, value) and
                    not re.search(None_pattern, value) and
                    not re.search(invalid_int_pattern, value)) or re.search(function_call_pattern, value):
                filtered_toggles.append(toggle)
        else:
            filtered_toggles.append(toggle)

    return filtered_toggles


def filter_toggles(toggles, language, file_contents):
    keywords = language_keywords.get(language, [])
    filtered_toggles = [t for t in toggles if t is not None and t != ""]

    filtered_toggles = [t for t in filtered_toggles if no_invalid_chars(t)]

    filtered_toggles = [t for t in filtered_toggles if not is_pure_number_or_dash_underscore(t)]

    filtered_toggles = [t for t in filtered_toggles if len(t) > 10]

    filtered_toggles = [t for t in filtered_toggles if t not in keywords]
    filtered_toggles = filter_substrings(filtered_toggles, file_contents)
    filtered_toggles = filter_wrong_values(filtered_toggles, file_contents)

    return filtered_toggles


def apply_combined_regexes(combined_content, language):
    toggles = set()
    patterns = regexes.get(language)
    if patterns:
        for pattern in patterns.keys():
            compiled_pattern = re.compile(patterns[pattern])
            matches = compiled_pattern.finditer(combined_content)
            for match in matches:
                toggle = match.group('toggle')
                if toggle[0] == '\"' and toggle[-1] == '\"':
                    toggle = toggle[1:-1]
                toggles.add(toggle)
    return toggles


def get_language_from_extension(file_path):
    if file_path.endswith('.py'):
        return 'python'
    elif file_path.endswith('.cs'):
        return 'csharp'
    elif file_path.endswith('.java'):
        return 'java'
    elif file_path.endswith('.go'):
        return 'golang'
    elif file_path.endswith('.cpp') or file_path.endswith('.cc'):
        return "c++"
    return None


def remove_comments(content, language):
    """Remove comment lines based on the language."""
    comment_pattern = comment_regexes.get(language)
    if comment_pattern:
        content = re.sub(comment_pattern, '', content, flags=re.MULTILINE)
    return content


def extract_toggles_from_config_files(config_files):
    toggle_list = []
    for conf_file in config_files:
        with open(conf_file, 'r', encoding='utf-8') as file:
            file_content = file.read()
            language = get_language_from_extension(conf_file)
            file_content = remove_comments(file_content, language)
            toggle_list.append(file_content)
    toggle_list = list(filter(None, toggle_list))
    combined_content = "\n".join(toggle_list)
    if config_files:
        language = get_language_from_extension(config_files[0])
        toggles = apply_combined_regexes(combined_content, language)
        filtered_toggles = filter_toggles(list(toggles), language, combined_content)
        filtered_toggles = list(set(filtered_toggles))
        return filtered_toggles
    return []


if __name__ == "__main__":
    # config_files_path = "../getToggleTests/example-config-files/cadence-constants.go"
    # config_files_path = "../getToggleTests/example-config-files/chrome-feature.cc"
    # config_files_path = "../toggle_extractor/example-config-files/dawn-toggles.cpp"
    config_files_path = "../toggle_extractor/example-config-files/opensearch-FeatureFlags.java"
    # config_files_path = "../getToggleTests/example-config-files/pytorch-proxy.py"
    # config_files_path = "../getToggleTests/example-config-files/sdb2-feature.java"
    # config_files_path = "../toggle_extractor/example-config-files/sentry-server.py"
    # config_files_path = "../toggle_extractor/example-config-files/temporal-constants.go"
    # config_files_path = "../getToggleTests/example-config-files/vtest-FeatureFlag.cs"
    # config_files_path = "../toggle_extractor/example-config-files/bitwarden-server-Constants.cs"
    config_files = [config_files_path]

    extracted_toggles = extract_toggles_from_config_files(config_files)

    print("Extracted Toggles:", extracted_toggles)
    print("Extracted Toggles length:", len(extracted_toggles))
