general_toggle_var_patterns = {
    'pattern1': r'features.has\([^)"]*([^\n),]*)'
}

toggle_config_patterns = {
    'pattern2': r'"([^\n"]*:[^\n"]*)": False',
    'pattern3': r'"([^\n"]*:[^\n"]*)": True'
}

nested_toggle_patterns = {
    'and_condition1': r'and\s*features.has\([^)]*\)',
    'and_condition2': r'\s*features.has\([^)]*\) and',
    'or_condition1': r'\s*features.has\([^)]*\) or',
    'or_condition2': r'or\s*features.has\([^)]*\)'
}

general_patterns = {
    'whitespace': r'\s*features.has\([^)"]*([^\n),]*)',
}

spread_toggle_patterns = {
    'parent_finder': [r'class (.*?)\:\n((?!.*class).*?\n)*?.*?%s']
}
