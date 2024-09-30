general_toggle_var_patterns = {
    'pattern1': r'features.has\([^)"]*([^\n),]*)'
}

toggle_config_patterns = {
    'pattern2': r'"([^\n"]*:[^\n"]*)": False',
    'pattern3': r'"([^\n"]*:[^\n"]*)": True'
}

nested_toggle_patterns = {
    'return_and': r'return\s+(.*?)\s+and',
    'if_and': r'if\s+(.*?)\s+and',
    'return_or': r'return\s+(.*?)\s+or',
    'if_or': r'if\s+(.*?)\s+or',

    'or_enter': r' or\s+(.*?)\n',
    'and_enter': r' and\s+(.*?)\n'
}

general_patterns = {
    'whitespace': r'\s*features.has\([^)"]*([^\n),]*)',
}

spread_toggle_patterns = {
    'parent_finder': [r'class (.*?)\:\n((?!.*class).*?\n)*?.*?%s']
}

enum_toggle_patterns = {
    'enum_def': [r'class\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(\s*Enum\s*\)'],
    'in_enum': r'class\s+(\w+)\(Enum\):\s*([^#]*)'
}