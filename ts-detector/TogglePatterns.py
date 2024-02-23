general_toggle_var_patterns = {
    'pattern_key': r'switches\:\:([k][A-Z][a-z,A-Z]*)'
}

toggle_patterns = {
    'const_char': r'const char (k[A-Z][a-z,A-Z]*)'
}

nested_toggle_patterns = {
    'if_condition': r'if\s*\(.*?\}',
    'else_condition': r'else\s*\(.*?\}',
    'elseif_condition': r'elseif\s*\(.*?\}'
}