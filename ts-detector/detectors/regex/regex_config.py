config_regex_patterns = {
    "toggle_definition": r"(?i)(toggle|feature|flag)\s*[:=]\s*\w+", 
    "parent_finder": r"(?i)(parent_toggle|base_toggle)\s*[:=]\s*\w+",  
}
spread_toggle_patterns = {
    "parent_finder": [
        r"(?i)(toggle|feature|flag)\s*[:=]\s*\w+", 
        r"(?i)(parent_toggle|base_toggle)\s*[:=]\s*\w+", 
    ]
}