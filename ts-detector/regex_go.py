general_toggle_var_patterns = {
    'pattern1': r'\n*(Enable.*): DynamicBool{' #< this is only checked on project cadence for now
}

toggle_config_patterns = {
    'pattern1': r'const char (k[A-Z][a-z,A-Z]*)'
}

nested_toggle_patterns = {
    'if_condition': r'if\s+.*?\}',
    'else_condition': r'else\s+.*?\}',
    'elseif_condition': r'else if\s+.*?\}'
}

spread_toggle_patterns = {
    'parent_finder': [r'package (\w)*\n']
}
file_extensions = ['.go']