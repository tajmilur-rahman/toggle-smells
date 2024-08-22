import re


def extract_variables(content):
    """
    Extracts all potential variable names from the content of a configuration file.

    Args:
        content (str): The content of the configuration file.

    Returns:
        list of str: List of extracted variable names.
    """
    # Regex patterns to capture variable declarations with possible spaces and type annotations
    variable_pattern = [
        r'\b(?:bool|boolean|var|const|let|int|float|double|char|auto|final)\s+([\w_]+)',
        r'\b(?:[\w<>\[\]]+)\s+([\w_]+)\s*(?:=|\()',
        r'\b(?:boolean|Boolean|Setting<Boolean>|String|int|float|double|char|long)\s+([\w_]+)\b',
        r'\b(?:public|protected|private)?\s*(?:static)?\s*(?:final)?\s*[\w<>\[\]]+\s+([\w_]+)\s*(?:=|\()'
    ]

    # Handle variable declarations with optional spaces and potential type annotations
    assignment_pattern = r'\b([\w_]+)\s*:\s*(?:bool|boolean|Flag|FeatureFlag|Toggle)\s*=\s*(true|false|True|False|0|1)'

    # Capture variables declared without explicit type (Python, Go, etc.)
    assignment_without_type_pattern = r'\b([\w_]+)\s*=\s*(true|false|True|False|0|1)'

    # Handle string-based feature flags in C++ or similar (const char type)
    string_feature_flag_pattern = r'\b(?:const\s+char)\s+([\w_]+)\s*\[\s*\]'

    # Extract variable names
    for pattern in variable_pattern:
        variable_names = re.findall(pattern, content)
    assignment_names = re.findall(assignment_pattern, content)
    assignment_without_type_names = re.findall(assignment_without_type_pattern, content)
    string_feature_flag_names = re.findall(string_feature_flag_pattern, content)

    # Combine and deduplicate variable names
    all_vars = set(variable_names + assignment_names + assignment_without_type_names + string_feature_flag_names)

    return list(all_vars)


def identify_boolean_variables(variable_names, content):
    """
    Identifies variables that are likely to be booleans or custom boolean-like types.

    Args:
        variable_names (list of str): List of variable names.
        content (str): The content of the configuration file.

    Returns:
        list of str: List of variable names that are likely to be boolean.
    """
    boolean_vars = []

    # Regex patterns to identify booleans or custom boolean types with possible spaces
    boolean_patterns = [
        r'\b(?:true|false|True|False)\b',
        r'\b(?:bool|boolean|Flag|FeatureFlag|Toggle)\b',
        r'\b(?:struct|class|type)\s+[\w_]+\s*{.*}\s*;',
        r'boolean \w*'
    ]

    for var in variable_names:
        # Check if variable is assigned a boolean value or if it's a custom boolean type
        for pattern in boolean_patterns:
            if re.search(fr'{var}\s*=\s*{pattern}', content):
                boolean_vars.append(var)
                break

    return boolean_vars


def check_feature_flag_names(variable_names):
    """
    Checks variable names against general feature flag naming conventions.

    Args:
        variable_names (list of str): List of variable names.

    Returns:
        list of str: List of variable names that match general feature flag naming conventions.
    """
    feature_flag_patterns = [
        r'\b(enable|disable|toggle|flag|feature)[\w_]*\b',
        r'\b[kK][\w_]+',  # for patterns like kEnableFeature
        r'[\w_-]+[:.][\w_-]+'  # for patterns like organizations:feature or flags.feature
    ]

    feature_flags = []

    for var in variable_names:
        for pattern in feature_flag_patterns:
            if re.search(pattern, var):
                feature_flags.append(var)
                break

    return feature_flags


def extract_feature_flags_from_file(file_path):
    """
    Extracts potential feature flag names from a given configuration file.

    Args:
        file_path (str): Path to the configuration file.

    Returns:
        list of str: List of potential feature flag names.
    """
    with open(file_path, 'r') as file:
        content = file.read()

    # Step 1: Extract all variable names
    variable_names = extract_variables(content)
    print(variable_names)

    # Step 2: Identify boolean variables
    boolean_vars = identify_boolean_variables(variable_names, content)

    # Step 3: Check for feature flag naming conventions
    feature_flags = check_feature_flag_names(variable_names)

    # Step 4: Combine both lists and remove duplicates
    combined_flags = list(set(boolean_vars + feature_flags))

    return combined_flags

# Example usage:
# file_path = '../example-config-files/chrome-feature.cc'
file_path = '../example-config-files/opensearch-FeatureFlags.java'
feature_flags = extract_feature_flags_from_file(file_path)
print(feature_flags)