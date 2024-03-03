general_toggle_var_patterns = {
    'pattern1': r'switches\:\:([k][A-Z][a-z,A-Z]*)'
}

toggle_config_patterns = {
    'pattern1': r'const char (k[A-Z][a-z,A-Z]*)'
}

nested_toggle_patterns = {
    'if_condition': r'if\s*\(.*?\}',
    'else_condition': r'else\s*\(.*?\}',
    'elseif_condition': r'elseif\s*\(.*?\}'
}

spread_toggle_patterns = {
    'parent_finder': [r'class (.*) \{(.|\n)*%s']
}
file_extensions = ['.py']