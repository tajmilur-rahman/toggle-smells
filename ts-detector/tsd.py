"""Main Module"""
import sys
import glob
import re

import t_utils

try:
    lang = sys.argv[1]
except:
    lang = None

try:
    source_path = sys.argv[2]
except:
    source_path = None

try:
    t_conf_file = sys.argv[3]
except:
    t_conf_file = None

try:
    t_usage = sys.argv[4]
except:
    t_usage = None


def is_valid_regex(pattern):
    try:
        re.compile(pattern)
        return True
    except re.error:
        return False


def get_user_string_input(prompt):
    res = input(prompt).strip()
    return res


def get_user_choice(prompt, option_list):
    for i in range(len(option_list)):
        print(i + 1, ") ", option_list[i])

    selected = get_user_string_input(prompt)

    while selected.isdigit() and int(selected) > len(option_list) + 1 or int(selected) < 1:
        print("Please enter valid number from 1 - ", len(option_list))
        for i in range(len(option_list)):
            print(i + 1, ") ", option_list[i])
        selected = get_user_string_input(prompt)

    return selected


def get_repeated_string(prompt):
    user_inputs = []
    while True:
        user_input = get_user_string_input(prompt + " or press Enter to finish): ")
        if user_input == '':
            break
        if is_valid_regex(user_input):
            user_inputs.append(user_input)
            print("Current list of values:", user_inputs)
        else:
            print("Invalid regular expression. Please try again.")
    return user_inputs


predefined = {
    "1": {
        "lang": "c++",
        "name": "C++ Chromium",
    },
    "2": {
        "lang": "c++",
        "name": "C++ Dawn",
    },
    "3": {
        "lang": "go",
        "name": "Go  Uber Cadence",
    },
    "4": {
        "lang": "Java",
        "name": "Java OpenSearch",
    },
    "5": {
        "lang": "python",
        "name": "Python OpenSearch",
    },
    "6": {
        "lang": "js",
        "name": "JS React",
    },
}

usage_list = ["dead", "spread", "mixed", "nested"]
# Usage: python3 tsd.py <language> </source/path> <config_file_postfix> <toggle_usage_type>
# Usage: python3 tsd.py C++ /Users/taj/Documents/Research/Data/chromium/ui/base switches.cc dead
if __name__ == "__main__":
    selected = get_user_choice(
        "Select predefined projects, enter number only:",
        [
            "C++ Chromium",
            "C++ Dawn",
            "Go  Uber Cadence",
            "Java OpenSearch",
            "Python Sentry",
            "JS React",
            "Self Input",
        ],
    )

    source_path = get_user_string_input("Enter the source path: ").rstrip("/")
    print("Your source path is {}".format(source_path))

    t_conf_file = get_user_string_input("Enter the config file: ")
    print("Your config file postfix is {}".format(t_conf_file))

    t_usage_index = get_user_choice(
        "Enter the toggle usage type: ",
        usage_list
    )

    t_usage = usage_list[int(t_usage_index) - 1]
    print("Your toggle usage is {}".format(t_usage))

    regex_p = {
        "general_pattern": [],
        "config_pattern": []
    }
    if selected == "7":
        lang = get_user_string_input("Enter the programming language: ")
        print("Your language is {}".format(lang))

        general_pattern = get_repeated_string("Please enter your toggles general usage pattern, how they are used, "
                                              "Make sure they are reg ex format, with r''"
                                              "e.g: r'GetBoolProperty.*\(.*.(.*)\)'")

        config_pattern = get_repeated_string("Please enter your toggles config pattern, how they are defined in the "                                     
                                             "Make sure they are reg ex format, with r''"
                                             "config file, e.g: r'.*(Enable.*): DynamicBool{'")

        regex_p["general_pattern"] = general_pattern
        regex_p["config_pattern"] = config_pattern

    else:
        lang = predefined[selected]["lang"]

    print(
        "Language: " + lang + ", Source path: " + source_path + ", Config file pattern: " + t_conf_file + ", Toggle usage pattern: " + t_usage)

    config_files = glob.glob(f'{source_path}/**/*{t_conf_file}', recursive=True)

    if lang.lower() == "c++":
        c_files = glob.glob(f'{source_path}/**/*.cc', recursive=True)
        cpp_files = glob.glob(f'{source_path}/**/*.cpp', recursive=True)
        code_files = c_files + cpp_files
    elif lang.lower() == "go":
        code_files = glob.glob(f'{source_path}/**/*.go', recursive=True)
    elif lang.lower() == "java":
        code_files = glob.glob(f'{source_path}/**/*.java', recursive=True)
    elif lang.lower() == "python":
        code_files = glob.glob(f'{source_path}/**/*.py', recursive=True)
    elif lang.lower() == "js":
        code_files = glob.glob(f'{source_path}/**/*.js', recursive=True)
    else:
        config_files = None
        code_files = None

    detectedToggles = t_utils.detect(lang, code_files, config_files, t_usage, regex_p)
    print(detectedToggles)
