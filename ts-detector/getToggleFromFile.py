import re

# Enhancing the provided functions

def extract_variables_and_values_enhanced(content):
    """
    Extracts potential variable names and their assigned values from the content of a configuration file, with enhanced patterns.

    Args:
        content (str): The content of the configuration file.

    Returns:
        tuple: List of extracted variable names, and a dictionary of variables with their assigned values.
    """
    # Enhanced regex patterns to capture variable declarations and assignments
    variable_patterns = [
        r'\b(?:bool|boolean|var|const|let|int|float|double|char|auto|final|String|static)\s+([\w_]+)',
        r'\b(?:[\w<>\[\]]+)\s+([\w_]+)\s*(?:=|\()',
        r'\b(?:boolean|Boolean|Setting<Boolean>|String|int|float|double|char|long)\s+([\w_]+)\b',
        r'\b(?:public|protected|private)?\s*(?:static)?\s*(?:final)?\s*[\w<>\[\]]+\s+([\w_]+)\s*(?:=|\()'
    ]

    # Enhanced assignment patterns for feature flags or boolean-like variables
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


def identify_boolean_variables_enhanced(variable_names, variable_values):
    """
    Identifies variables that are likely to be booleans or custom boolean-like types.

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
            if value.lower() in ['true', 'false', '0', '1']:
                boolean_vars.append(var)

    return boolean_vars


def check_feature_flag_names_enhanced(variable_names, variable_values):
    """
    Checks variable names and values against general feature flag naming conventions, with enhanced patterns.

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

    feature_flags = []

    for var in variable_names:
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


def extract_feature_flags_from_file_enhanced(file_path):
    """
    Extracts potential feature flag names from a given configuration file, with enhanced detection.

    Args:
        file_path (str): Path to the configuration file.

    Returns:
        list of str: List of potential feature flag names.
    """
    with open(file_path, 'r') as file:
        content = file.read()

    # Extract all variables and values
    variable_names, variable_values = extract_variables_and_values_enhanced(content)

    # Identify boolean variables
    boolean_vars = identify_boolean_variables_enhanced(variable_names, variable_values)

    # Check for feature flag naming conventions
    feature_flags = check_feature_flag_names_enhanced(variable_names, variable_values)

    # Combine both lists and remove duplicates
    combined_flags = list(set(boolean_vars + feature_flags))

    return combined_flags
# Example usage:
# file_path = '../getToggleTests/example-config-files/chrome-feature.cc'
# file_path = '../getToggleTests/example-config-files/opensearch-FeatureFlags.java'
# file_path = '../getToggleTests/example-config-files/pytorch-proxy.py'
file_path = '../getToggleTests/example-config-files/sentry-server.py'
# file_path = '../getToggleTests/example-config-files/azure-pipelines-agent-featureflag.cs'
# file_path = '../getToggleTests/example-config-files/temporal-constants.go'
# file_path = '../getToggleTests/example-config-files/dawn-toggles.cpp'

feature_flags = extract_feature_flags_from_file_enhanced(file_path)
print("Feature Flags:", feature_flags)
