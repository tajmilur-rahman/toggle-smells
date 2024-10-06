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
            "if_statement": r"if\s*.*?\s*\{",
            "elif_statement": r"else\s*if\s*.*?\s*\{",
            "variable_assignment": r"\w+\s*=\s*.*?;",
            "return_statement": r"return\s+.*?;"
        }
    }

    regex_patterns = regex_patterns_by_language.get(lang.lower())

    if not regex_patterns:
        raise ValueError(f"Unsupported language: {lang}")

    for code_file, content in zip(code_files, code_files_contents):
        if lang != "go" and lang != "python":
            content = content.replace("\n", "")

        code_snippets = []
        for pattern_name, pattern in regex_patterns.items():
            if lang != "go" and lang != "python":
                code_snippets += re.findall(pattern, content)
            else:
                code_snippets += re.findall(pattern, content, re.MULTILINE)


        var_assignment = []
        if lang != "go" and lang != "python":
            p = r"\s\w*\s*=\s+.*?;"
            var_assignment = re.findall(p, content)
            var_assignment = list(set(var_assignment))

        toggleDict = {}
        for toggle in toggles:
            toggleDict[toggle] = [toggle]
            for var in var_assignment:
                if toggle in var:
                    toggleDict[toggle].extend(re.findall(r"\s(\w*)\s*=\s+.*?;", var))


        for snippet in code_snippets:
            matched_toggles = []
            for t in toggleDict:
                for alias in toggleDict[t]:
                    if alias in snippet:
                        if lang != "python" and ("|" in snippet or "&" in snippet):
                            matched_toggles.append(t)
                        elif lang == "python" and ("or" in snippet or "and" in snippet):
                            matched_toggles.append(t)
                        break

            if matched_toggles:
                nested_toggles.extend(matched_toggles)
                total_count_toggles += len(matched_toggles)

    nested_toggles_data = {
        "nested_toggles": nested_toggles,
        "total_count_toggles": total_count_toggles
    }

    return nested_toggles_data


def format_nested_toggles_data(nested_toggles_data):
    unique_toggles = list(set(nested_toggles_data['nested_toggles']))
    unique_toggles.sort()
    result = {
        "toggles": unique_toggles,
        "qty": len(unique_toggles),
    }
    return result

