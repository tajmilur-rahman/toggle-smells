general_toggle_var_patterns = {
    'pattern1': r'\s(\w*) = Setting\.boolSetting\(' #< this is only checked on project opensearch for now
}

toggle_config_patterns = {
    'pattern1': r'const char (k[A-Z][a-z,A-Z]*)'
}

nested_toggle_patterns = {
    'if_condition': r'if\s*\(.*?\}',
    'else_condition': r'else\s*\(.*?\}',
    'elseif_condition': r'elseif\s*\(.*?\}'
}

combinatory_toggle_pattens = {
    'pattern1': r'(%s)((\n|.?){0,1}(&&))',
    'pattern2': r'&&\n\s*(%s)',
    'pattern3': r'\n\s*&&\s*(%s)',
}

spread_toggle_patterns = {
    'parent_finder': [r'class (.*) \{(.|\n)*%s']
}
file_extensions = ['.java']