general_toggle_var_patterns = {
    'pattern1': r'FeatureFlags.isEnabled\(FeatureFlags.(.*?)\)',
}

toggle_config_patterns = {
    'pattern1': r'\s(\w*) = Setting\.boolSetting\(',  # < this is only checked on project opensearch for now
    'pattern2': r' (\w*) =\n? "opensearch.experimental'
}

nested_toggle_patterns = {
    'if_condition': r'if[^}]*?}',
    'else_condition': r'else[^}]*?}',
    'elseif_condition': r'else if[^}]*?}'
}

general_patterns = {
    'whitespace': r'FeatureFlags.isEnabled\(FeatureFlags.(.*?)\)',
}

spread_toggle_patterns = {
    'parent_finder': [r'class (.*( extends|implements \w*)*) \{(.|\n)*%s']
}

enum_toggle_patterns = {
    'enum_def': [r'enum\s+([A-Za-z_][A-Za-z0-9_]*)'],
    "in_enum": r'enum\s+(\w+)\s*{([^}]*)};',

}