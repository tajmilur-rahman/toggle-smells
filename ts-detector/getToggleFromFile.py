import re

regexes = {
    'python': {
        'declare': r'(?P<toggle>\w+)\s*(?:\:\s*(?P<type>[^\s=]+))?\s*=\s*',
        'capital_identifiers': r'(?P<toggle>[A-Z][A-Z0-9_-]{2,})',
        'dict_keys': r'[{,]\s*(?P<toggle>(?:[\'\"][^\'\"]*[\'\"]|[^:]+?))\s*:'
    },
    'csharp': {
        'declare': (
            r'(public|protected|private\s+protected|private)\s+(?:static\s+|const\s+|readonly\s+)*(\w+(?:\s*<[^>]+>)?)\s+(?P<toggle>\w+)\s*(?=\s*(=|;|\[))'
        ),
        'capital_identifiers': r'(?P<toggle>[A-Z][A-Z0-9_-]{2,})',
        'dict_keys': r'[{,]\s*(?P<toggle>(?:@"[^"]*"|"[^"]*"|\'[^\']*\'|[^,\s]+?))\s*,'
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
        'dict_keys': r'\bput\s*\(\s*(?P<toggle>"[^"]*"|\'[^\']*\'|[^,\s]+?)\s*,'
    },
    'golang': {
        'declare': (
            r'(?:var\s+(?P<toggle>\w+)\s*(?:\s+(?P<type>[^\s=]+))?\s*(?:=\s*.*)?|'
            r'(?P<toggle2>\w+)\s*(?:\s+(?P<type2>[^\s=]+))?\s*:=\s*.*)'
        ),
        'capital_identifiers': r'(?P<toggle>[A-Z][A-Z0-9_-]{2,})',
        'dict_keys': r'[{,]\s*(?P<toggle>(?:`[^`]*`|"[^"]*"|\'[^\']*\'|[\w.]+?))\s*:'
    },
    'cpp': {
        'declare': (
            r'(?:(?:const|static|volatile|extern|mutable)\s+)*'
            r'(?P<type>(?:[\w:]+)(?:\s*<[^>;]+>)?'
            r'(?:\s*::\s*[\w:]+)*(?:\s*[\*&])?)\s+'
            r'(?P<toggle>\w+)\s*'
            r'(?=\s*(=|;|\[))'
        ),
        'capital_identifiers': r'(?P<toggle>[A-Z][A-Z0-9_-]{2,})',
        'dict_keys': r'[{,]\s*(?P<toggle>(?:"[^"]*"|\'[^\']*\'|[^,\s]+?))\s*,',
        'toggle_names': r'{\s*Toggle::(?P<toggle>\w+),'
    }
}

def apply_combined_regexes(combined_content, language):
    toggles = set()

    patterns = regexes.get(language)

    if patterns:
        # Apply each regex and collect results
        for pattern in patterns.keys():
            compiled_pattern = re.compile(patterns[pattern])
            matches = compiled_pattern.finditer(combined_content)
            for match in matches:
                toggle = match.group('toggle')
                print(match.group('toggle'))
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
        return 'cpp'
    return None

def extract_toggles_from_config_files(config_files):
    toggle_list = []
    for conf_file in config_files:
        with open(conf_file, 'r') as file:
            file_content = file.read()
            toggle_list.append(file_content)

    toggle_list = list(filter(None, toggle_list))
    combined_content = "\n".join(toggle_list)

    if config_files:
        language = get_language_from_extension(config_files[0])

        toggles = apply_combined_regexes(combined_content, language)
        return list(toggles)

    return []

# Example usage
if __name__ == "__main__":
    config_files_path = "../getToggleTests/example-config-files/bitwarden-server-Constants.cs"  # Replace with the path to your config files

    config_files = [config_files_path]

    extracted_toggles = extract_toggles_from_config_files(config_files)

    print("Extracted Toggles:", extracted_toggles)

