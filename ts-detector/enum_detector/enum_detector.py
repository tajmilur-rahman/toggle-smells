import re

# Dictionary containing regex patterns for different languages
REGEX_PATTERNS = {
    'java': r'enum\s+(\w+)\s*{([^}]*)}',  # Java enum
    'python': r'class\s+(\w+)\(Enum\):\s*([^#]*)',  # Python Enum class
    'go': r'const\s*\((.*?)\)',  # Go const block with iota
    'cpp': r'enum\s+(\w+)?\s*{([^}]*)}',  # C++/C enum
    'csharp': r'enum\s+(\w+)\s*{([^}]*)}',  # C# enum
    'c': r'enum\s+(\w+)?\s*{([^}]*)}'  # C enum
}


def extract_enum_members(code, language):
    """
    Extracts the enum members from a given code string based on the specified language.

    Args:
        code (str): The content of a code file as a string.
        language (str): The programming language ('java', 'python', 'go', 'cpp', 'csharp', 'c').

    Returns:
        dict: A dictionary where keys are enum names and values are lists of enum members.
    """
    enum_members = {}

    if language not in REGEX_PATTERNS:
        raise ValueError(f"Unsupported language: {language}")

    # Get the regex pattern for the specified language
    enum_pattern = re.compile(REGEX_PATTERNS[language], re.DOTALL)

    if language == 'java' or language == 'cpp' or language == 'csharp' or language == 'c':
        # For Java, C++, C#, and C, the enum members are within curly braces
        for match in enum_pattern.finditer(code):
            enum_name = match.group(1) or "UnnamedEnum"
            members_block = match.group(2)
            members = [member.strip() for member in members_block.split(',') if member.strip()]
            enum_members[enum_name] = members

    elif language == 'python':
        # For Python, enum members are defined as class variables
        for match in enum_pattern.finditer(code):
            enum_name = match.group(1)
            members_block = match.group(2)
            members = re.findall(r'(\w+)\s*=\s*\d+', members_block)
            enum_members[enum_name] = members

    elif language == 'go':
        # For Go, enum-like members are defined in const blocks
        for match in enum_pattern.finditer(code):
            members_block = match.group(1)
            members = [member.split('=')[0].strip() for member in members_block.split('\n') if member.strip()]
            enum_members['GoEnum'] = members

    return enum_members


def is_enum_member(code, var_name, language):
    """
    Checks if a given variable name is a member of any enum in the code for a given language.

    Args:
        code (str): The content of a code file as a string.
        var_name (str): The variable name to check.
        language (str): The programming language ('java', 'python', 'go', 'cpp', 'csharp', 'c').

    Returns:
        bool: True if the variable name is a member of any enum, False otherwise.
    """
    enums = extract_enum_members(code, language)
    for enum_name, members in enums.items():
        if var_name in members:
            return True
    return False
