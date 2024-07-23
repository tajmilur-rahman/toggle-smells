# how it is used
general_toggle_var_patterns = {
    'pattern': r'\n*(Enable.*): DynamicBool{',
    'pattern1': r'GetBoolProperty.*\(.*.(.*)\)'
}

# how it looks in config file
toggle_config_patterns = {
    'pattern1': r'.*(Enable.*): DynamicBool{',
}

# if/else patterns
nested_toggle_patterns = {
    'if_condition': r'\tif\s*[^}]*\}',
    'else_condition': r'} else\s*[^}]*\}',
    'elseif_condition': r'} else if\s*[^}]*\}'
}


general_patterns = {
    'whitespace': r'([\w*\.]*\w*Enable\w*)',
}

# how a parent looks like shouldn't need user input
spread_toggle_patterns = {
    'parent_finder': [r'\npackage (.*)(\n)'],
}

