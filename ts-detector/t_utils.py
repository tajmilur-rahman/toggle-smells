import detectors.regex.regex_c as c_patterns
import detectors.regex.regex_java as j_patterns
import detectors.regex.regex_python as py_patterns
import detectors.regex.regex_go as go_patterns
import detectors.regex.regex_csharp as csharp_patterns
from collections import defaultdict

import detectors.toggle_extractor.toggle_extractor as toggle_extractor

from detectors.enum_detector.enum_detector import *
import detectors.mixed_detector.mixed_detector as md

import detectors.helper as helper

import detectors.spread_detector.spread_detector as sd
import detectors.dead_detector.dead_detector as dd
import detectors.nested_detector.nested_detector as nd
import os

language_map = {
    "c++": c_patterns,
    "java": j_patterns,
    "python": py_patterns,
    "go": go_patterns,
    "csharp": csharp_patterns
}


def detect(lang, code_files, t_config_files, t_usage):
    if lang is None:
        raise ValueError("Language is not defined.")

    if code_files is None:
        raise ValueError("A list of code files is required.")

    if t_config_files is None:
        raise ValueError("A list of config files is required.")

    toggle_source_files = t_config_files if lang == "config" else code_files

    if t_usage == "dead":
        return extract_dead_toggles(lang, toggle_source_files, t_config_files)
    elif t_usage == "spread":
        return extract_spread_toggles(lang, toggle_source_files, t_config_files)
    elif t_usage == "nested":
        return extract_nested_toggles(lang, toggle_source_files, t_config_files)
    elif t_usage == "enum":
        return extract_enum_toggles(lang, toggle_source_files, t_config_files)
    elif t_usage == "mixed" and lang != "config":
        return extract_mixed_toggles(lang, toggle_source_files)
    else:
        print(f"The '{t_usage}' toggle pattern is not supported for {lang}.")
        return []
    
def process_config_toggles(toggles, pattern_type):
    """
    Process config toggles based on the toggle type.
    :param toggles: List of extracted toggles
    :param pattern_type: Type of toggle pattern (e.g., dead, nested, enum, spread)
    :return: Dictionary with processed toggle data
    """
    if pattern_type == "dead":
        return {"dead_toggles": toggles}
    elif pattern_type == "nested":
        return {"nested_toggles": toggles}
    elif pattern_type == "enum":
        return {"enum_toggles": list(toggles), "qty": len(toggles)}
    elif pattern_type == "spread":
        return {"spread_toggles": toggles}
    else:
        raise ValueError(f"Unsupported pattern type: {pattern_type}")
    
def extract_dead_toggles(lang, code_files, t_config_files):
    print("extracting dead toggles")
    toggles = get_toggles_from_config_files(t_config_files, lang)
    
    if lang == "config":
        # Default usage_count = 0 for config toggles (update logic can be added later)
        formatted_toggles = [toggle for toggle in toggles]
    else:
        code_files_contents = helper.get_code_file_contents(lang, code_files)
        dead_toggles = dd.find_dead_toggles(toggles, code_files, code_files_contents)
        formatted_toggles = dd.format_dead_toggles_data(dead_toggles)
    
    return formatted_toggles


def extract_nested_toggles(lang, code_files, t_config_files):
    print("extracting nested toggles")

    toggles = toggle_extractor.extract_toggles_from_config_files(t_config_files)
    nested_toggles = defaultdict(list)

    if lang == "config":
        for config_file in t_config_files:
            if not os.path.exists(config_file):
                print(f"Warning: File not found - {config_file}")
                continue

            with open(config_file, 'r') as file:
                content = file.read()
                for toggle in toggles:
                    dependencies = [
                        dep for dep in toggles if dep in content and dep != toggle
                    ]
                    if dependencies:
                        relative_path = os.path.relpath(config_file)
                        nested_toggles[toggle].append({
                            relative_path: dependencies
                        })
    else:
        # Language-specific projects
        code_files_contents = helper.get_code_file_contents(lang, code_files)
        nested_data = nd.process_code_files(lang, code_files, code_files_contents, toggles, proximity=3)
        nested_toggles = nested_data["nested_toggles"]

    return nd.format_nested_toggles_data({"nested_toggles": nested_toggles})

def extract_spread_toggles(lang, code_files, t_config_files):
    print("extracting spread toggles")

    spread_toggles = defaultdict(list)
    toggles = get_toggles_from_config_files(t_config_files, lang)

    if lang == "config":
        for code_file in code_files:
            if not os.path.exists(code_file):
                print(f"Warning: File not found - {code_file}")
                continue

            with open(code_file, 'r') as file:
                content = file.read()
                for toggle in toggles:
                    count = content.count(toggle)
                    if count > 0:
                        relative_path = os.path.relpath(code_file)
                        spread_toggles[toggle].append({
                            "file": relative_path,
                            "count": count
                        })

    # Process Language-Specific Projects
    if lang != "config":
        for code_file in code_files:
            if not os.path.exists(code_file):
                print(f"Warning: File not found - {code_file}")
                continue

            with open(code_file, 'r') as file:
                content = file.read()
                for toggle in toggles:
                    count = content.count(toggle)
                    if count > 0:
                        relative_path = os.path.relpath(code_file)
                        spread_toggles[toggle].append({
                            "file": relative_path,
                            "count": count
                        })
        spread_toggles = {
            toggle: occurrences
            for toggle, occurrences in spread_toggles.items()
            if len({entry["file"] for entry in occurrences}) > 1  
        }

    if lang == "config":
        for toggle in toggles:
            if toggle not in spread_toggles:
                spread_toggles[toggle] = []

    formatted_toggles = {
        "toggles": spread_toggles,
        "qty": len(spread_toggles)
    }
    return formatted_toggles

def extract_mixed_toggles(lang, code_files):
    print("extracting mixed toggles")

    mixed_toggles = defaultdict(list)
    code_files_contents = helper.get_code_file_contents(lang, code_files)
    mixed_patterns = helper.get_mixed_toggle_var_patterns(lang)

    md.process_code_files(code_files, code_files_contents, mixed_patterns, mixed_toggles)

    return md.format_mixed_toggles_data(mixed_toggles)

def extract_enum_toggles(lang, code_files, t_config_files):
    print("extracting enum toggles")
    # get all toggle names
    # dictionary to store spread toggle data
    toggle_lookup = defaultdict(list)
    # get all toggles from config files as a set
    toggles = set(get_toggles_from_config_files(t_config_files, lang))

    if lang == "config":
        formatted_toggles = [toggle for toggle in toggles]
        return formatted_toggles

    code_files_contents = helper.get_code_file_contents(lang, code_files)

    res_toggles = []
    # find all enums and check if name in it
    for code_file, file_content in zip(code_files, code_files_contents):
        res = is_enum_member(file_content, toggles, lang)
        for toggle in res:
            toggle_lookup[toggle].append(code_file)
            res_toggles.append(toggle)

    res = {
        "toggles": list(res_toggles),
        "qty": len(res_toggles)
    }

    return res

def get_toggles_from_config_files(config_files, lang=None):
    """
    Wrapper around toggle extraction to manage and return toggles from files.
    """
    return toggle_extractor.extract_toggles_from_config_files(config_files, lang=lang)