import json
import re


def format_python_toggles(toggles):
    return [f'"{toggle}"' for toggle in toggles]


def find_dead_toggles(toggles, code_files, code_files_contents):
    dead_toggles = toggles.copy()

    for code_file, file_content in zip(code_files, code_files_contents):
        for toggle in toggles:
            matches = re.findall(toggle, file_content)
            if matches:
                dead_toggles.remove(toggle)

    return dead_toggles


def format_dead_toggles_data(dead_toggles):
    dead_toggles_data = {
        "dead_toggles": dead_toggles,
        "total_count": len(dead_toggles)
    }
    return json.dumps(dead_toggles_data, indent=2)
