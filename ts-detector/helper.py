import regex_c as c_patterns
import regex_java as j_patterns
import regex_python as py_patterns
import regex_go as go_patterns
import regex_csharp as csharp_patterns
import re

language_map = {
    "c++": c_patterns,
    "java": j_patterns,
    "python": py_patterns,
    "go": go_patterns,
    "csharp": csharp_patterns
}

def get_code_file_contents(lang, code_files):
    code_files_contents = []
    for file in code_files:
        if lang.lower() == "c++":
            if 'switch' not in file and 'feature' not in file:
                with open(file, 'rb') as f:
                    try:
                        content = f.read().decode('utf-8')
                        code_files_contents.append(content)
                    except UnicodeDecodeError:
                        pass
        else:
            with open(file, 'rb') as f:
                try:
                    content = f.read().decode('utf-8')
                    code_files_contents.append(content)
                except UnicodeDecodeError:
                    pass
    return code_files_contents


def getFileName(lang, path):
    if lang == "python":
        regex = r"[^\/]*\.py"
        return re.findall(regex, path)[0]
    elif lang == "js":
        regex = r"[^\/]*\.js"
        return re.findall(regex, path)[0]
    elif lang == 'java':
        regex = r"[^\/]*\.java"
        return re.findall(regex, path)[0]
    elif lang == 'go':
        regex = r"[^\/]*\.go"
        return re.findall(regex, path)[0]

    return path


def get_directive_patterns(lang):
    return language_map[lang.lower()].mixed_toggle_patterns['if_directive']


def get_toggle_config_patterns(lang):
    return list(language_map[lang.lower()].toggle_config_patterns.values())


def get_general_toggle_var_patterns(lang):
    return list(language_map[lang.lower()].general_toggle_var_patterns.values())


def get_nested_toggle_patterns(lang):
    return list(language_map[lang.lower()].nested_toggle_patterns.values())


def get_mixed_toggle_var_patterns(lang):
    return list(language_map[lang.lower()].mixed_toggle_patterns.values())


def get_spread_toggle_var_patterns(lang):
    return language_map[lang.lower()].spread_toggle_patterns


def get_nested_toggle_var_patterns(lang):
    return language_map[lang.lower()].nested_toggle_patterns


def get_enum_toggle_var_patterns(lang):
    return language_map[lang.lower()].enum_toggle_patterns
