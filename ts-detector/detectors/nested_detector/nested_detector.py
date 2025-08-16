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
            'return_and': r"return\s+(.*?)\s+and",
            'if_and': r"if\s+(.*?)\s+and",
            'return_or': r"return\s+(.*?)\s+or",
            'if_or': r"if\s+(.*?)\s+or",
            'or_enter': r" or\s+(.*?)\n",
            'and_enter': r" and\s+(.*?)\n",
            'multi_line_condition': r"(\b(and|or)\b.*\\n)+",  
            'function_call': r"\b\w+\((.*?)(and|or)(.*?)\)",
            'assign_and': r"[^=]=\s+(.*?) and",
            'assign_or': r"[^=]=\s+(.*?) or",
            'nested_if': r"if\s.*:\s*if\s.*:",  
            'nested_return': r"return\s+.*(?:and|or).*",  
            'elif_condition': r"\belif\s+.*:",
            'condition': r"(if|elif|return|and|or)\s+(.*?)\b",
            'logical_and': r"\b(and|&&)\b",
            'logical_or': r"\b(or|\|\|)\b"
        },       
        "java": {
            'if_statement': r"if\s*\(.*?\)\s*\{",
            'nested_if': r"if\s*\(.*?\)\s*\{.*if\s*\(.*?\)\s*\{", 
            'conditional_operator': r"\?.*?:",  
            'logical_combination': r"\b&&|\|\|\b", 
            'function_call': r"\b\w+\((.*?)(&&|\|\|)(.*?)\)",  
            'variable_assignment': r"\w+\s*=\s*.*?;",
            'return_statement': r"return\s+.*?;",
            'condition': r"(if|return)\s*\(.*?\)"
        },
        "csharp": {
            'if_statement': r"if\s*\(.*?\)\s*\{",
            'nested_if': r"if\s*\(.*?\)\s*\{.*if\s*\(.*?\)\s*\{", 
            'conditional_expression': r"\?.*?:", 
            'logical_combination': r"\b&&|\|\|\b", 
            'function_call': r"\b\w+\((.*?)(&&|\|\|)(.*?)\)",  
            'variable_assignment': r"\w+\s*=\s*.*?;",
            'return_statement': r"return\s+.*?;",
            'condition': r"(if|return)\s*\(.*?\)"
        },
        "c++": {
            'if_statement': r"if\s*\(.*?\)\s*\{",
            'nested_if': r"if\s*\(.*?\)\s*\{.*if\s*\(.*?\)\s*\{", 
            'conditional_operator': r"\?.*?:", 
            'logical_combination': r"\b&&|\|\|\b", 
            'function_call': r"\b\w+\((.*?)(&&|\|\|)(.*?)\)", 
            'variable_assignment': r"\w+\s*=\s*.*?;",
            'return_statement': r"return\s+.*?;",
            'condition': r"(if|return)\s*\(.*?\)"
        },
        "go": {
            'if_statement': r"if\s*.*?\s*\{",
            'nested_if': r"if\s*.*?\s*\{.*if\s*.*?\s*\{", 
            'logical_combination': r"\b&&|\|\|\b", 
            'function_call': r"\b\w+\((.*?)(&&|\|\|)(.*?)\)",  
            'variable_assignment': r"\w+\s*=\s*.*?;",
            'return_statement': r"return\s+.*?;",
            'condition': r"(if|return)\s*.*?\{"
        }
    }

    regex_patterns = regex_patterns_by_language.get(lang.lower())
    if not regex_patterns:
        raise ValueError(f"Unsupported language: {lang}")

    compiled_patterns = {name: re.compile(pattern) for name, pattern in regex_patterns.items()}

    for code_file, content in zip(code_files, code_files_contents):
        lines = content.splitlines()
        num_lines = len(lines)

        toggle_lines = [i for i, line in enumerate(lines) if any(toggle in line for toggle in toggles)]

        for line_idx in toggle_lines:
            start_idx = max(0, line_idx - proximity)
            end_idx = min(num_lines, line_idx + proximity + 1)
            nearby_lines = lines[start_idx:end_idx]

            # Analyze dependencies using regex patterns
            dependencies = set()
            matched_toggles = set()
            for nearby_line in nearby_lines:
                for pattern_name, pattern in compiled_patterns.items():
                    if pattern.search(nearby_line): 
                        matched_toggles.update(
                            toggle for toggle in toggles if toggle in nearby_line
                        )
                        dependencies.update(
                            dep for dep in toggles if dep in nearby_line
                        )

            for toggle in matched_toggles:
                if dependencies:
                    nested_toggles[toggle][code_file] = list(dependencies - {toggle})  
                    total_count_toggles += len(dependencies - {toggle})

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