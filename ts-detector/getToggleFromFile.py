import re
import os


def extract_variables_and_values_refined(content):
    """
    Extracts potential variable names and their assigned values from the content of a configuration file, with refined patterns.

    Args:
        content (str): The content of the configuration file.

    Returns:
        tuple: List of extracted variable names, and a dictionary of variables with their assigned values.
    """
    # Refined regex patterns to capture variable declarations and assignments
    variable_patterns = [
        r'\b(?:bool|boolean|var|const|let|int|float|double|char|auto|final|String|static)\s+([\w_]+)',
        r'\b(?:[\w<>\[\]]+)\s+([\w_]+)\s*(?:=|\()',
        r'\b(?:boolean|Boolean|Setting<Boolean>|String|int|float|double|char|long)\s+([\w_]+)\b',
        r'\b(?:public|protected|private)?\s*(?:static)?\s*(?:final)?\s*[\w<>\[\]]+\s+([\w_]+)\s*(?:=|\()'
    ]

    # Refined assignment patterns
    assignment_pattern = r'\b([\w_]+)\s*:\s*(?:bool|boolean|Flag|FeatureFlag|Toggle)\s*=\s*(true|false|True|False|0|1)'
    assignment_without_type_pattern = r'\b([\w_]+)\s*=\s*(true|false|True|False|0|1)'
    string_value_pattern = r'\b([\w_]+)\s*=\s*"([\w_:.:-]+)"'

    variable_names = []
    variable_values = {}

    # Extract variables and assignments
    for pattern in variable_patterns:
        variable_names.extend(re.findall(pattern, content))

    # Extract assignments and values
    assignments = re.findall(assignment_pattern, content)
    assignments_without_type = re.findall(assignment_without_type_pattern, content)
    string_values = re.findall(string_value_pattern, content)

    for name, value in assignments:
        variable_values[name] = value

    for name, value in assignments_without_type:
        variable_values[name] = value

    for name, value in string_values:
        variable_values[name] = value

    return variable_names, variable_values


def identify_boolean_variables_refined(variable_names, variable_values):
    """
    Identifies variables that are likely to be booleans or custom boolean-like types, with more refined checks.

    Args:
        variable_names (list of str): List of variable names.
        variable_values (dict): Dictionary of variable names with their assigned values.

    Returns:
        list of str: List of variable names that are likely to be boolean.
    """
    boolean_vars = []

    for var in variable_names:
        if var in variable_values:
            value = variable_values[var]
            if value.lower() in ['true', 'false', '0', '1'] and len(var) > 2:  # Exclude very short variables
                boolean_vars.append(var)

    return boolean_vars


def check_feature_flag_names_refined(variable_names, variable_values):
    """
    Checks variable names and values against general feature flag naming conventions, with exclusions for common non-flag names.

    Args:
        variable_names (list of str): List of variable names.
        variable_values (dict): Dictionary of variable names with their assigned values.

    Returns:
        list of str: List of variable names that match general feature flag naming conventions.
    """
    feature_flag_patterns = [
        r'\b(enable|disable|toggle|flag|feature|proxy)[\w_]*\b',  # Common feature flag keywords
        r'\b[kK][\w_]+',  # Patterns like kEnableFeature
        r'[\w_-]+[:.][\w_-]+',  # Config-style patterns like feature.enable
        r'[\w_]+[_-][\w_]+',  # Patterns like check_mutable_operations
    ]

    # Common non-feature flag names to exclude (e.g., size, index)
    exclusions = ['size', 'index', 'count', 'length', 'int64', 'float', 'char', '__len__', '__getitem__', '__enter__', '__len__', '__repr__', '__call__', '__bool__', '__iter__', '__torch_function__', '__abs__', '__init__', '__exit__', '__getattr__', 'to_bool', '__all__']

    feature_flags = []

    for var in variable_names:
        if var not in exclusions:
            for pattern in feature_flag_patterns:
                if re.search(pattern, var):
                    feature_flags.append(var)
                    break

    # Also check string values against feature flag patterns
    for var, value in variable_values.items():
        for pattern in feature_flag_patterns:
            if re.search(pattern, value):
                feature_flags.append(var)
                break

    return list(set(feature_flags))


def extract_feature_flags_from_file_refined(file_path):
    """
    Extracts potential feature flag names from a given configuration file, with refined detection logic to reduce false positives.

    Args:
        file_path (str): Path to the configuration file.

    Returns:
        list of str: List of potential feature flag names.
    """
    with open(file_path, 'r') as file:
        content = file.read()

    # Extract all variables and values
    variable_names, variable_values = extract_variables_and_values_refined(content)

    # Identify boolean variables
    boolean_vars = identify_boolean_variables_refined(variable_names, variable_values)

    # Check for feature flag naming conventions
    feature_flags = check_feature_flag_names_refined(variable_names, variable_values)

    # Combine both lists and remove duplicates
    combined_flags = list(set(boolean_vars + feature_flags))

    return combined_flags

# Example usage:
file_path1 = '../getToggleTests/example-config-files/chrome-feature.cc'
file_path2 = '../getToggleTests/example-config-files/opensearch-FeatureFlags.java'
file_path3 = '../getToggleTests/example-config-files/pytorch-proxy.py'
file_path4 = '../getToggleTests/example-config-files/sentry-server.py'
file_path5 = '../getToggleTests/example-config-files/azure-pipelines-agent-featureflag.cs'
file_path6 = '../getToggleTests/example-config-files/temporal-constants.go'
file_path7 = '../getToggleTests/example-config-files/dawn-toggles.cpp'

extracted_files = [file_path1, file_path2, file_path3, file_path4, file_path5, file_path6, file_path7]

refined_file_flags_final = {}
for filepath in extracted_files:
    feature_flags_detected = extract_feature_flags_from_file_refined(filepath)
    if feature_flags_detected:
        refined_file_flags_final[os.path.basename(filepath)] = feature_flags_detected

for i in refined_file_flags_final:
 print(i)
 print(refined_file_flags_final[i])
