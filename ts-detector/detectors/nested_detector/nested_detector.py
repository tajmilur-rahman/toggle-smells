import json
import re
from .. import helper


def process_code_files(lang, code_files, code_files_contents, nested_patterns, nested_toggles, regex_patterns):
    for code_file, content in zip(code_files, code_files_contents):
        for pattern in nested_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                code_lines = extract_code_lines(lang, match)
                populate_nested_toggles(nested_toggles, lang, code_file, code_lines, regex_patterns)


def extract_code_lines(lang, match):
    if lang == "python":
        return [match.replace('\n', "")]
    return match.split('\n')


def populate_nested_toggles(nested_toggles, lang, code_file, code_lines, regex_patterns):
    filename = helper.getFileName(lang, code_file)
    if filename not in nested_toggles:
        nested_toggles[filename] = []

    for line in code_lines:
        for pattern in regex_patterns["general_pattern"]:
            nested_toggles[filename].extend(re.findall(pattern, line))



def clean_nested_toggles(nested_toggles):
    distinct_toggles = set()
    to_delete = []

    for key in list(nested_toggles.keys()):
        nested_toggles[key] = list(dict.fromkeys(nested_toggles[key]))
        distinct_toggles.update(nested_toggles[key])
        if len(nested_toggles[key]) == 0:
            to_delete.append(key)

    for key in to_delete:
        del nested_toggles[key]

    return nested_toggles, distinct_toggles


def format_nested_toggles_data(nested_toggles):
    total_count_path = len(nested_toggles[0])
    total_count_toggles = len(set(toggle for toggles in nested_toggles for toggle in toggles))

    nested_toggles_serializable = [list(toggles) if isinstance(toggles, set) else toggles for toggles in nested_toggles]

    nested_toggles_data = {
        "nested_toggles": nested_toggles_serializable[1],
        "total_count_path": total_count_path,
        "total_count_toggles": total_count_toggles
    }

    return json.dumps(nested_toggles_data, indent=2)
