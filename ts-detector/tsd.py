import sys
import glob
import argparse
import t_utils


def auto_detect_language(config_files):
    for config_file in config_files:
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
            elif "function " in content:
                return "js"
    return None

def main():
    parser = argparse.ArgumentParser(description='Detect usage patterns in source code.')
    parser.add_argument('-p', '--source-path', required=True, help='Source code directory path')
    parser.add_argument('-c', '--config-path', required=True, help='Configuration file path')
    parser.add_argument('-o', '--output', required=False, help='Output file path')
    parser.add_argument('-t', '--toggle-usage', required=True, choices=["dead", "spread", "mixed", "nested"], help='Toggle usage pattern to detect')
    parser.add_argument('-l', '--language', required=False, help='Programming language (optional, auto-detect if not provided)')

    args = parser.parse_args()

    source_path = args.source_path.rstrip("/")
    config_path = args.config_path
    output_path = args.output
    toggle_usage = args.toggle_usage
    lang = args.language

    if not lang:
        config_files = glob.glob(f'{config_path}/**/*', recursive=True)
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
    elif lang.lower() == "js":
        code_files = glob.glob(f'{source_path}/**/*.js', recursive=True)
    else:
        print("Unsupported language. Exiting.")
        sys.exit(1)

    regex_p = {
        "general_pattern": [],
        "config_pattern": []
    }

    detectedToggles = t_utils.detect(lang, code_files, config_files, toggle_usage, regex_p)

    if output_path:
        with open(output_path, 'w') as f:
            f.write(str(detectedToggles))
        print(f"Output written to {output_path}")
    else:
        print(detectedToggles)


if __name__ == "__main__":
    main()