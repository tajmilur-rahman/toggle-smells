import re


def extract_variables_and_values(content):
    """
    Extracts all potential variable names and their assigned values from the content of a configuration file.

    Args:
        content (str): The content of the configuration file.

    Returns:
        tuple: List of extracted variable names, and a dictionary of variables with their assigned values.
    """
    # Regex patterns to capture variable declarations with possible spaces and type annotations
    variable_patterns = [
        r'\b(?:bool|boolean|var|const|let|int|float|double|char|auto|final|String|static)\s+([\w_]+)',
        r'\b(?:[\w<>\[\]]+)\s+([\w_]+)\s*(?:=|\()',
        r'\b(?:boolean|Boolean|Setting<Boolean>|String|int|float|double|char|long)\s+([\w_]+)\b',
        r'\b(?:public|protected|private)?\s*(?:static)?\s*(?:final)?\s*[\w<>\[\]]+\s+([\w_]+)\s*(?:=|\()'
    ]

    # Capture variables and their values
    assignment_pattern = r'\b([\w_]+)\s*:\s*(?:bool|boolean|Flag|FeatureFlag|Toggle)\s*=\s*(true|false|True|False|0|1)'
    assignment_without_type_pattern = r'\b([\w_]+)\s*=\s*(true|false|True|False|0|1)'
    string_value_pattern = r'\b([\w_]+)\s*=\s*"([\w_:.:-]+)"'

    variable_names = []
    variable_values = {}

    for pattern in variable_patterns:
        variable_names.extend(re.findall(pattern, content))

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


def identify_boolean_variables(variable_names, variable_values):
    """
    Identifies variables that are likely to be booleans or custom boolean-like types.

    Args:
        variable_names (list of str): List of variable names.
        variable_values (dict): Dictionary of variable names with their assigned values.

    Returns:
        list of str: List of variable names that are likely to be boolean.
    """
    boolean_vars = []

    # Check boolean values directly
    for var in variable_names:
        if var in variable_values:
            value = variable_values[var]
            if value.lower() in ['true', 'false', '0', '1']:
                boolean_vars.append(var)

    return boolean_vars


def check_feature_flag_names(variable_names, variable_values):
    """
    Checks variable names and values against general feature flag naming conventions.

    Args:
        variable_names (list of str): List of variable names.
        variable_values (dict): Dictionary of variable names with their assigned values.

    Returns:
        list of str: List of variable names that match general feature flag naming conventions.
    """
    feature_flag_patterns = [
        r'\b(enable|disable|toggle|flag|feature|proxy)[\w_]*\b',
        r'\b[kK][\w_]+',  # for patterns like kEnableFeature
        r'[\w_-]+[:.][\w_-]+',  # for patterns like organizations:feature or flags.feature
        r'[\w_]+[_-][\w_]+',  # for patterns like check_mutable_operations
    ]

    feature_flags = []

    # Check variable names against patterns
    for var in variable_names:
        for pattern in feature_flag_patterns:
            if re.search(pattern, var):
                feature_flags.append(var)
                break

    # Check string values against patterns
    for var, value in variable_values.items():
        for pattern in feature_flag_patterns:
            if re.search(pattern, value):
                feature_flags.append(var)
                break

    # Remove duplicates
    return list(set(feature_flags))


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

    # Step 1: Extract all variable names and their values
    variable_names, variable_values = extract_variables_and_values(content)
    print("Variable Names:", variable_names)
    print("Variable Values:", variable_values)

    # Step 2: Identify boolean variables
    boolean_vars = identify_boolean_variables(variable_names, variable_values)

    # Step 3: Check for feature flag naming conventions
    feature_flags = check_feature_flag_names(variable_names, variable_values)

    # Step 4: Combine both lists and remove duplicates
    combined_flags = list(set(boolean_vars + feature_flags))

    return combined_flags

# Example usage:
# file_path = '../example-config-files/chrome-feature.cc'
# file_path = '../example-config-files/opensearch-FeatureFlags.java'
# file_path = '../example-config-files/pytorch-proxy.py'
file_path = '../example-config-files/sentry-server.py'

feature_flags = extract_feature_flags_from_file(file_path)
print("Feature Flags:", feature_flags)
