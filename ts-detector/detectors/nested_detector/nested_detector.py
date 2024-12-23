from collections import defaultdict
import re

def process_code_files(lang, code_files, code_files_contents, toggles, proximity=3):
    """
    Processes code files to identify nested toggles and their dependencies.
    """
    nested_toggles = defaultdict(dict)  # toggle -> {file_path -> [dependencies]}
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
            'assign_or': r'[^=]=\s+(.*?) or',
            'if_condition': r'\bif\s+.*:',
            'elif_condition': r'\belif\s+.*:',
            'logical_and': r'\b(and|&&)\b',
            'logical_or': r'\b(or|\|\|)\b',
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
        lines = content.splitlines() 

        for line_idx, line in enumerate(lines):
            if any(re.search(pattern, line) for pattern in regex_patterns.values()):
                # Extract toggles in the condition
                matched_toggles = [toggle for toggle in toggles if toggle in line]
                start_idx = max(0, line_idx - proximity)
                end_idx = min(len(lines), line_idx + proximity + 1)
                nearby_lines = lines[start_idx:end_idx]
                dependencies = set()
                for nearby_line in nearby_lines:
                    dependencies.update(
                        toggle for toggle in toggles if toggle in nearby_line and toggle not in matched_toggles
                    )

                # Update nested toggles mapping
                for toggle in matched_toggles:
                    if dependencies:
                        nested_toggles[toggle][code_file] = list(dependencies)
                        total_count_toggles += len(dependencies)

    return {
        "nested_toggles": nested_toggles,
        "qty": total_count_toggles
    }


def format_nested_toggles_data(nested_toggles_data):
    nested_toggles = nested_toggles_data["nested_toggles"]
    formatted_toggles = defaultdict(list)

    for toggle, file_dependencies in nested_toggles.items():
        for file_path, dependencies in file_dependencies.items():
            if dependencies:
                formatted_toggles[toggle].append({file_path: list(set(dependencies))})

    return {
        "toggles": dict(formatted_toggles),
        "qty": len(formatted_toggles)
    }