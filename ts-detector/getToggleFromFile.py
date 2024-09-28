import re
import os

language_patterns = {
    'cs': {
        'variable_patterns': [
            r'\b(?:bool|boolean|var|const|let|int|float|double|char|String)\s+([\w_]+)',
            r'FeatureFlag\.(\w+)',  # Common C# feature flag access
            r'\b([\w_]+)\s*=\s*(true|false)',  # Boolean assignments
        ],
        'flag_patterns': [
            r'if\s*\(\s*FeatureFlags\.(\w+)',  # Checking feature flags
            r'\b(enable|disable|toggle|flag|feature)[\w_]*',  # Feature-related keywords
        ]
    },
    'go': {
        'variable_patterns': [
            r'\b(?:bool|var)\s+([\w_]+)',  # Go boolean or variable declaration
            r'\b([\w_]+)\s*:=\s*(true|false)',  # Boolean assignment
        ],
        'flag_patterns': [
            r'if\s+(\w+)\s*==\s*(true|false)',  # Feature toggle in conditional statements
            r'\b(enable|disable|toggle|flag|feature)[\w_]*',
        ]
    },
    'java': {
        'variable_patterns': [
            r'\b(?:boolean|Boolean|String|int|float|long|final|var)\s+([\w_]+)',  # Java variable declaration
            r'\b([\w_]+)\s*=\s*(true|false|True|False)',  # Boolean assignment
        ],
        'flag_patterns': [
            r'FeatureFlags\.(\w+)',  # Accessing feature flags in Java
            r'if\s*\(\s*FeatureFlags\.(\w+)',  # Checking feature flags
            r'\b(enable|disable|toggle|flag|feature)[\w_]*',
        ]
    },
    'cpp': {
        'variable_patterns': [
            r'\b(?:bool|int|float|double|char)\s+([\w_]+)',  # C++ variable declaration
            r'base::Feature\(\s*"(\w+)"',  # C++ feature flag declaration
        ],
        'flag_patterns': [
            r'if\s*\(\s*IsEnabled\("(\w+)"\)',  # Checking feature flags in C++
            r'\b(enable|disable|toggle|flag|feature)[\w_]*',
        ]
    },
    'py': {
        'variable_patterns': [
            r'\b([\w_]+)\s*=\s*(True|False|true|false)',  # Python boolean assignment
        ],
        'flag_patterns': [
            r'if\s+feature_flags\.(\w+)',  # Checking feature flags in Python
            r'\b(enable|disable|toggle|flag|feature)[\w_]*',
        ]
    }
}

# Function to detect feature flags using language-specific patterns
def detect_language_specific_flags(content, filetype):
    flags = set()
    if filetype in language_patterns:
        patterns = language_patterns[filetype]

        # Detect variables
        for pattern in patterns['variable_patterns']:
            matches = re.findall(pattern, content)
            flags.update(matches)

        # Detect flags or feature-related checks
        for pattern in patterns['flag_patterns']:
            matches = re.findall(pattern, content)
            flags.update(matches)

    return list(flags)

# Mapping file extensions to their corresponding language for easier detection
filetype_mapping = {
    'cs': 'cs',
    'go': 'go',
    'java': 'java',
    'cpp': 'cpp',
    'cc': 'cpp',
    'py': 'py'
}




# Example usage:
file_path1 = '../getToggleTests/example-config-files/chrome-feature.cc'
file_path2 = '../getToggleTests/example-config-files/opensearch-FeatureFlags.java'
file_path3 = '../getToggleTests/example-config-files/pytorch-proxy.py'
file_path4 = '../getToggleTests/example-config-files/sentry-server.py'
file_path5 = '../getToggleTests/example-config-files/azure-pipelines-agent-featureflag.cs'
file_path6 = '../getToggleTests/example-config-files/temporal-constants.go'
file_path7 = '../getToggleTests/example-config-files/dawn-toggles.cpp'

extracted_files = [file_path1, file_path2, file_path3, file_path4, file_path5, file_path6, file_path7]

def read_file_content(filepath):
    with open(filepath, 'r') as file:
        return file.read()

# Apply the language-specific feature flag detection
language_specific_file_flags = {}
for filepath in extracted_files:
    ext = filepath.split('.')[-1].lower()
    filetype = filetype_mapping.get(ext)
    if filetype:
        content = read_file_content(filepath)
        feature_flags_detected = detect_language_specific_flags(content, filetype)
        if feature_flags_detected:
            language_specific_file_flags[os.path.basename(filepath)] = feature_flags_detected

# for i in language_specific_file_flags:
#  print(i)
#  print(language_specific_file_flags[i])