import re


def format_python_toggles(toggles):
    return [f'"{toggle}"' for toggle in toggles]


def find_dead_toggles(toggles, code_files, code_files_contents):
    dead_toggles = set(toggles)

    for file_content in code_files_contents:
        for toggle in list(dead_toggles):
            if re.search(toggle, file_content):
                dead_toggles.remove(toggle)
            if not dead_toggles:
                return []

    return list(dead_toggles)


def format_dead_toggles_data(dead_toggles):
    dead_toggles_data = {
        "toggles": dead_toggles,
        "qty": len(dead_toggles)
    }
    return dead_toggles_data
