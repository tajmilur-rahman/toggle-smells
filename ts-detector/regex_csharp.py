general_toggle_var_patterns = {
    'pattern1': r'switches\:\:([k][A-Z][a-z,A-Z]*)'
}

toggle_config_patterns = {
    'pattern1': r'const char (k[A-Z][a-z,A-Z]*)'
}

nested_toggle_patterns = {
    'if_condition': r'if\s*\(.*?[k][A-Z][a-z,A-Z]*\}',
    'else_condition': r'else\s*\(.*?[k][A-Z][a-z,A-Z]*\}',
    'elseif_condition': r'elseif\s*\(.*?[k][A-Z][a-z,A-Z]*\}'
}

mixed_toggle_patterns = {
    'if_directive': r'#if\s+BUILDFLAG\s*\(\s*(\w+)\s*\)',
}

general_patterns = {
    'char_seq': r'.*?\}',
    'whitespace': r'\s*(k[A-Z][a-zA-Z0-9]*)',
    'condition_count': r'\b(if|else|elseif)\b'
}

spread_toggle_patterns = {
    'parent_finder': [r'(class .*) \{(.|\n)*%s', r'(namespace .*) \{(.|\n)*%s']
}

enum_toggle_patterns = {
    'enum_def': [r'enum\s+(class\s+)?([A-Za-z_][A-Za-z0-9_]*)'],
    "in_enum": r'enum\s+(\w+)?\s*{([^}]*)}',
}