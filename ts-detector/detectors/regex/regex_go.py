# how it looks in config file
toggle_config_patterns = {
    'pattern1': r'.*(Enable.*): DynamicBool\{',
    'pattern2': r'(\w*enable\w*) = \w*Bool\w*',
    'pattern3': r'(\w*enable\w*): \w*Bool\w*',
}

# if/else patterns
nested_toggle_patterns = {
    'if_condition': r'\tif\s*[^}]*\}',
    'else_condition': r'} else\s*[^}]*\}',
    'elseif_condition': r'} else if\s*[^}]*\}'
}

# how a parent looks like shouldn't need user input
spread_toggle_patterns = {
    'parent_finder': [r'\npackage (.*)(\n)'],
}

enum_toggle_patterns = {
    'enum_def': [r'const\s*\([\s\S]*?\b([A-Za-z_][A-Za-z0-9_]*)\s*=\s*iota'],
    "in_enum": r'const\s*\((.*?)\)',
}