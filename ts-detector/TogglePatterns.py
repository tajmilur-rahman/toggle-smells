general_usage_patterns = {
    #'char_seq': r'.*?\}',
    #'pattern_key': r'[::][k]\w*\b',
    'pattern_key': r'switches[::][k][A-Z][A-Z,a-z]*',
    #'condition_count': r'\b(if|else|elseif)\b'
}

toggle_patterns = {
    #'whitespace': r'\s*k[A-Z].*',
    #'feature': r'\::Feature k[A-Z].*',
    'const_char': r'const char k[A-Z].*'
}

dead_toggle_patterns = {
    'colon': r'\::k[A-Z].*',
    'parentheses': r'\s*\(k[A-Z]',
    'switches': r'switches\::k[A-Z].*?\)',
    'if_condition': r'\s*if\s*\(k[A-Z].*\)'
}

nested_toggle_patterns = {
    'if_condition': r'if\s*\(.*?\}',
    'else_condition': r'else\s*\(.*?\}',
    'elseif_condition': r'elseif\s*\(.*?\}'
}