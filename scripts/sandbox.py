# Refining regex by tailoring it for specific languages to reduce false positives
# We will define language-specific patterns for feature flag detection
import os
import re


def get_language_specific_patterns(filetype):
    """ Return language-specific patterns for detecting feature flags. """
    if filetype == 'cs':  # C# patterns
        return [
            r'FeatureFlags\.(\w+)',  # Common C# feature flag pattern
            r'if\s*\(\s*FeatureFlags\.(\w+)',  # Conditional based flags
            r'(\w+Flag)\s*=\s*(true|false)'  # Feature flags set as booleans
        ]
    elif filetype == 'py':  # Python patterns
        return [
            r'feature_flags\.(\w+)',  # Common Python feature flag usage
            r'if\s+(\w+)\s*==\s*(True|False)',  # Python boolean checks
            r'(\w+_flag)\s*=\s*(True|False)'  # Common flag pattern in Python
        ]
    elif filetype == 'java':  # Java patterns
        return [
            r'FeatureFlags\.(\w+)',  # Common Java pattern for feature flags
            r'if\s*\(\s*FeatureFlags\.(\w+)',  # Conditional feature flag check
            r'(\w+Flag)\s*=\s*(true|false)'  # Boolean flag pattern
        ]
    elif filetype == 'go':  # Go patterns
        return [
            r'featureFlag\.(\w+)',  # Go feature flag usage
            r'if\s+(\w+)\s*==\s*true',  # Go boolean checks
            r'(\w+Flag)\s*=\s*(true|false)'  # Boolean flag in Go
        ]
    elif filetype in ['cpp', 'cc']:  # C++ patterns
        return [
            r'base::Feature\("(\w+)"',  # C++ base feature pattern
            r'IsEnabled\("(\w+)"\)',  # C++ IsEnabled check for feature flags
            r'(\w+Flag)\s*=\s*(true|false)'  # Common flag pattern in C++
        ]
    else:
        return []  # Default to no patterns if the language isn't recognized

# Modify the extraction function to apply language-specific patterns
def extract_feature_flags_from_file_language_specific(file_path):
    """Extract feature flags using language-specific regex patterns."""
    ext = file_path.split('.')[-1].lower()  # Get file extension
    patterns = get_language_specific_patterns(ext)

    with open(file_path, 'r') as file:
        content = file.read()

    feature_flags = set()
    # Apply each regex pattern for the specific language
    for pattern in patterns:
        matches = re.findall(pattern, content)
        feature_flags.update(matches)

    return list(feature_flags)



file_path1 = '../getToggleTests/example-config-files/chrome-feature.cc'
file_path2 = '../getToggleTests/example-config-files/opensearch-FeatureFlags.java'
file_path3 = '../getToggleTests/example-config-files/pytorch-proxy.py'
file_path4 = '../getToggleTests/example-config-files/sentry-server.py'
file_path5 = '../getToggleTests/example-config-files/azure-pipelines-agent-featureflag.cs'
file_path6 = '../getToggleTests/example-config-files/temporal-constants.go'
file_path7 = '../getToggleTests/example-config-files/dawn-toggles.cpp'

extracted_files = [file_path1, file_path2, file_path3, file_path4, file_path5, file_path6, file_path7]

# Apply this refined detection to all files
refined_file_flags = {}
for filepath in extracted_files:
    feature_flags_detected = extract_feature_flags_from_file_language_specific(filepath)
    if feature_flags_detected:
        refined_file_flags[os.path.basename(filepath)] = feature_flags_detected

print(refined_file_flags)