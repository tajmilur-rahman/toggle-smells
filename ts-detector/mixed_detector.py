import json
import re


def process_code_files(code_files, code_files_contents, mixed_patterns, mixed_toggles):
    for code_file, content in zip(code_files, code_files_contents):
        for pattern in mixed_patterns:
            matches = re.findall(pattern, content)
            count_occurrences(code_file, matches, mixed_toggles)


def count_occurrences(code_file, matches, mixed_toggles):
    for match in matches:
        mixed_toggles[match].append((code_file, matches.count(match)))


def format_mixed_toggles_data(mixed_toggles):
    mixed_toggles_data = {
        "mixed_toggles": mixed_toggles,
        "total_count": len(mixed_toggles)
    }
    return json.dumps(mixed_toggles_data, indent=2)
