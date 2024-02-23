"""Main Module"""
import sys
import glob

import ToggleUtils

source_path = sys.argv[1]
t_conf_file = sys.argv[2]
try:
    t_usage = sys.argv[3]
except:
    t_usage = ""
try:
    lang = sys.argv[4]
except:
    lang = ""

if __name__ == "__main__":
    source_path = source_path.rstrip("/")
    print("Source path: " + source_path + ", Config file pattern: " + t_conf_file + ", Toggle usage pattern: " + t_usage + ", Language: " + lang)
    config_files = glob.glob(f'{source_path}/**/*_{t_conf_file}', recursive=True)
    code_files = glob.glob(f'{source_path}/**/*.cc', recursive=True)

    deadToggles = ToggleUtils.detect(code_files, config_files, t_usage, lang)
    print(deadToggles)
