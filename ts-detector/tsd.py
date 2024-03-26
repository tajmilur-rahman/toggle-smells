"""Main Module"""
import sys
import glob

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

# Usage: python3 tsd.py <language> </source/path> <config_file_postfix> <toggle_usage_type>
# Usage: python3 tsd.py C++ /Users/taj/Documents/Research/Data/chromium/ui/base switches.cc dead
if __name__ == "__main__":
    source_path = source_path.rstrip("/")
    print("Language: " + lang + ", Source path: " + source_path + ", Config file pattern: " + t_conf_file + ", Toggle usage pattern: " + t_usage)

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

    detectedToggles = t_utils.detect(lang, code_files, config_files, t_usage)
    print(detectedToggles)
