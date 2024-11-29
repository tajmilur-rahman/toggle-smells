import json
import sys
import glob
import os
import argparse
import t_utils

patterns = ["dead", "spread", "nested", "mixed", "enum"]


def auto_detect_language(config_files):
    for config_file in config_files:
        file_extension = config_file.split('.')[-1]  # Get the file extension
        # Check for common programming language extensions
        if file_extension == "py":
            return "python"
        elif file_extension == "java":
            return "java"
        elif file_extension in ["cpp", "cc", "cxx", "hpp"]:
            return "c++"
        elif file_extension == "go":
            return "go"
        elif file_extension == "js":
            return "javascript"
        elif file_extension == "ts":
            return "typescript"
        elif file_extension == "cs":
            return "csharp"

        # If extension doesn't provide enough information, check content for more clues
        with open(config_file, 'r') as f:
            content = f.read()
            if "import java" in content:
                return "java"
            elif "#include <" in content:
                return "c++"
            elif "def " in content:
                return "python"
            elif "package main" in content:
                return "go"
            elif "function " in content or "console.log" in content:
                return "javascript"
            elif "namespace " in content or "using System" in content:
                return "csharp"

    return None


def detect_toggles_in_config(file_path):
    """
    Detect feature toggles in generic config files like `.properties`.
    """
    toggle_keywords = ["toggle", "feature", "flag"]  # Common keywords
    detected_toggles = []

    with open(file_path, 'r') as file:
        for line in file:
            if any(keyword in line for keyword in toggle_keywords):
                detected_toggles.append(line.strip())

    return detected_toggles


def main():
    parser = argparse.ArgumentParser(description='Detect usage patterns in source code.')
    parser.add_argument('-p', '--source-path', required=True, help='Source code directory path')
    parser.add_argument('-c', '--config-path', required=True, nargs='+',
                        help='Relative configuration file paths (relative to source path)')
    parser.add_argument('-o', '--output', required=False, help='Output file path')
    parser.add_argument('-t', '--toggle-usage', required=False, choices=patterns, help='Toggle usage pattern to detect')
    parser.add_argument('-l', '--language', required=False,
                        help='Programming language (optional, auto-detect if not provided)')

    args = parser.parse_args()

    source_path = args.source_path.rstrip("/")
    config_paths = [os.path.join(source_path, c) for c in args.config_path]
    output_path = args.output
    toggle_usage = args.toggle_usage
    lang = args.language

    if not lang:
        config_files = glob.glob(f'{config_paths[0]}', recursive=True)

        # Checking if none of the config files have language specific extension
        config_file_type = ""
        for config_file in config_files:
            file_extension = config_file.split('.')[-1]  # Get the file extension
            # Check for common programming language extensions
            if file_extension in ["properties", "conf", "cfg"]:
                config_file_type = "config"

        detected_lang = ""
        if config_file_type is not "config":
            detected_lang = auto_detect_language(config_files)

        if not detected_lang:
            print("Could not auto-detect language. Please provide it using the -l flag.")
            sys.exit(1)

    print(f"Language: {lang}, Source path: {source_path}, Config file pattern: {config_paths}, "
          f"Toggle usage pattern: {toggle_usage}")

    code_files = []
    config_files_paths = []
    for c in config_paths:
        config_files_paths.extend(glob.glob(f'{c}', recursive=True))

    if lang.lower() == "c++":
        c_files = glob.glob(f'{source_path}/**/*.cc', recursive=True)
        cpp_files = glob.glob(f'{source_path}/**/*.cpp', recursive=True)
        mm_files = glob.glob(f'{source_path}/**/*.mm', recursive=True)
        m_files = glob.glob(f'{source_path}/**/*.m', recursive=True)
        code_files = c_files + cpp_files + mm_files + m_files
    elif lang.lower() == "go":
        code_files = glob.glob(f'{source_path}/**/*.go', recursive=True)
    elif lang.lower() == "java":
        code_files = glob.glob(f'{source_path}/**/*.java', recursive=True)
    elif lang.lower() == "python":
        code_files = glob.glob(f'{source_path}/**/*.py', recursive=True)
    elif lang.lower() == "csharp":
        code_files = glob.glob(f'{source_path}/**/*.cs', recursive=True)
    else:
        print("Unsupported language. Exiting.")
        sys.exit(1)

    for config_file in config_files_paths:
        if config_file in code_files:
            code_files.remove(config_file)

    if toggle_usage:
        detected_toggles = t_utils.detect(lang, code_files or [], config_files_paths, toggle_usage)

        res = {toggle_usage: detected_toggles}
        res_json = json.dumps(res, indent=2)

        if output_path:
            with open(output_path, 'w') as f:
                f.write(str(res_json))
            print(f"Output written to {output_path}")
        else:
            print(res_json)

    else:
        res = {}
        for p in patterns:
            if p == "mixed" and lang.lower() != "c++":
                continue
            detected_toggles = t_utils.detect(lang, code_files or [], config_files_paths, p)

            res[p] = detected_toggles
        res_json = json.dumps(res, indent=2)
        if output_path:
            with open(output_path, 'w') as f:
                f.write(str(res_json))
            print(f"Output written to {output_path}")
        else:
            print(res_json)
    # TODO: Move this code inside utils
    # there is no such language called "config", handle the logic in an appropriate manner
    if lang == "config":
        # Process config files separately
        detected_toggles = []
        for config_file in config_files_paths:
            if os.path.exists(config_file):
                toggles = detect_toggles_in_config(config_file)
                detected_toggles.extend(toggles)
        if detected_toggles:
            print(f"Detected toggles in config files: {detected_toggles}")
        else:
            print("No toggles detected in config files.")
        return


if __name__ == "__main__":
    main()
