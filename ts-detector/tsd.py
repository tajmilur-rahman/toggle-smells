import sys
import glob
import argparse
import t_utils

patterns = ["dead", "spread", "mixed", "nested"]

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

def main():
    parser = argparse.ArgumentParser(description='Detect usage patterns in source code.')
    parser.add_argument('-p', '--source-path', required=True, help='Source code directory path')
    parser.add_argument('-c', '--config-path', required=True, help='Configuration file path')
    parser.add_argument('-o', '--output', required=False, help='Output file path')
    parser.add_argument('-t', '--toggle-usage', required=False, choices=patterns, help='Toggle usage pattern to detect')
    parser.add_argument('-l', '--language', required=False, help='Programming language (optional, auto-detect if not provided)')

    args = parser.parse_args()

    source_path = args.source_path.rstrip("/")
    config_path = args.config_path
    output_path = args.output
    toggle_usage = args.toggle_usage
    lang = args.language

    if not lang:
        config_files = glob.glob(f'{config_path}', recursive=True)
        lang = auto_detect_language(config_files)
        if not lang:
            print("Could not auto-detect language. Please provide it using the -l flag.")
            sys.exit(1)
    
    print(f"Language: {lang}, Source path: {source_path}, Config file pattern: {config_path}, Toggle usage pattern: {toggle_usage}")

    config_files = glob.glob(f'{config_path}/**/*', recursive=True)
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
    else:
        print("Unsupported language. Exiting.")
        sys.exit(1)

    if toggle_usage:
        detected_toggles = t_utils.detect(lang, code_files, config_files, toggle_usage, {})

        if output_path:
            with open(output_path, 'w') as f:
                f.write(str(detected_toggles))
            print(f"Output written to {output_path}")
        else:
            print(detected_toggles)

    else:
        for p in patterns:
            detected_toggles = t_utils.detect(lang, code_files, config_files, p, {})
            if output_path:
                with open(output_path+'/'+p, 'w') as f:
                    f.write(str(detected_toggles))
                print(f"Output written to {output_path}")
            else:
                print(detected_toggles)


if __name__ == "__main__":
    main()