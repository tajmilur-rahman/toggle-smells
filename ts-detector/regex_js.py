general_toggle_var_patterns = {
    'pattern1': r'[ |(](\w*)[ |)]',
}

toggle_config_patterns = {
    'pattern1': r'\n\s*(\w*),',
    'pattern2': r'export const (\w*) = false;',
    'pattern3': r'export const (\w*) = true;',
}

nested_toggle_patterns = {
    'if_condition': r'if[^}]*?}',
    'else_condition': r'else[^}]*?}',
    'elseif_condition': r'else if[^}]*?}'
}

combinatory_toggle_pattens = {
    'pattern1': r'(%s)((\n|.?){0,1}(&&))',
    'pattern2': r'&&\n\s*(%s)',
    'pattern3': r'\n\s*&&\s*(%s)',
}

general_patterns = {
    'whitespace': r'FeatureFlags.isEnabled\(FeatureFlags.(.*?)\)',
}

spread_toggle_patterns = {
    'parent_finder': [r'class (.*( extends|implements \w*)*) \{(.|\n)*%s']
}
