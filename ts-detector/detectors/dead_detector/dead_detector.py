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
                try:
                    dead_toggles.remove(toggle)
                except ValueError:
                    pass

    return dead_toggles


def format_dead_toggles_data(dead_toggles):
    dead_toggles_data = {
        "toggles": dead_toggles,
        "qty": len(dead_toggles)
    }
    return dead_toggles_data
