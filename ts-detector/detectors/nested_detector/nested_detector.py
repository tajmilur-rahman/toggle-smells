import re

def process_code_files(lang, code_files, code_files_contents, toggles):
    nested_toggles = []
    total_count_toggles = 0

    regex_patterns_by_language = {
        "python": {
            'return_and': r'return\s+(.*?)\s+and',
            'if_and': r'if\s+(.*?)\s+and',
            'return_or': r'return\s+(.*?)\s+or',
            'if_or': r'if\s+(.*?)\s+or',
            'or_enter': r' or\s+(.*?)\n',
            'and_enter': r' and\s+(.*?)\n',
            'enter_or': r'$\s+(.*?) or',
            'enter_and': r'$\s+(.*?) and',
            'assign_and': r'[^=]=\s+(.*?) and',
            'assign_or': r'[^=]=\s+(.*?) or'
        },
        "java": {
            "if_statement": r"if\s*\(.*?\)\s*\{",
            "elif_statement": r"else\s*if\s*\(.*?\)\s*\{",
            "variable_assignment": r"\w+\s*=\s*.*?;",
            "return_statement": r"return\s+.*?;"
        },
        "csharp": {
            "if_statement": r"if\s*\(.*?\)\s*\{",
            "elif_statement": r"else\s*if\s*\(.*?\)\s*\{",
            "variable_assignment": r"\w+\s*=\s*.*?;",
            "return_statement": r"return\s+.*?;"
        },
        "c++": {
            "if_statement": r"if\s*\(.*?\)\s*\{",
            "elif_statement": r"else\s*if\s*\(.*?\)\s*\{",
            "variable_assignment": r"\w+\s*=\s*.*?;",
            "return_statement": r"return\s+.*?;"
        },
        "go": {
            "if_statement": r"if\s*\(.*?\)\s*\{",
            "elif_statement": r"else\s*if\s*\(.*?\)\s*\{",
            "variable_assignment": r"\w+\s*=\s*.*?;",
            "return_statement": r"return\s+.*?;"
        }
    }

    regex_patterns = regex_patterns_by_language.get(lang.lower())

    if not regex_patterns:
        raise ValueError(f"Unsupported language: {lang}")

    for code_file, content in zip(code_files, code_files_contents):
        code_snippets = []
        for pattern_name, pattern in regex_patterns.items():
            code_snippets += re.findall(pattern, content, re.MULTILINE)

        for snippet in code_snippets:
            matched_toggles = [toggle for toggle in toggles if toggle in snippet]
            if matched_toggles:
                nested_toggles.extend(matched_toggles)
                total_count_toggles += len(matched_toggles)

    nested_toggles_data = {
        "nested_toggles": nested_toggles,
        "total_count_toggles": total_count_toggles
    }

    return nested_toggles_data


def format_nested_toggles_data(nested_toggles_data):
    unique_toggles = set(nested_toggles_data['nested_toggles'])
    result = {
        "qty": len(unique_toggles),
        "toggles": list(unique_toggles)
    }
    return result

