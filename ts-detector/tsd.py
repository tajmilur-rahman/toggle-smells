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
    print("Source path: " + source_path + ", Config file pattern: " + t_conf_file + ", Toggle usage pattern: " + t_usage + ", Language: " + lang)
    config_files = glob.glob(f'{source_path}/**/*_{t_conf_file}', recursive=True)
    code_files = glob.glob(f'{source_path}/**/*.cc', recursive=True)

    foundToggles = t_utils.detect(lang, code_files, config_files, t_usage)
    print(foundToggles)
