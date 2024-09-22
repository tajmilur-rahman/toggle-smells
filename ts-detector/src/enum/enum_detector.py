import re


def find_enums(code: str, lang: str):
    """Finds all enum definitions in the code based on the language."""
    enum_patterns = {
        "c++": r'enum\s+(\w+)\s*{([^}]*)};',
        'java': r'enum\s+(\w+)\s*{([^}]*)}',
        'go': r'type\s+(\w+)\s+int\s*\nconst\s+\([\s\S]*?iota',
        'python': r'class\s+(\w+)\(Enum\):\s*([\s\S]*?)(?=\n\n|\Z)'
    }

    pattern = enum_patterns.get(lang)

    return re.findall(pattern, code)


def find_variable_declarations(code: str, var_name: str):
    """ find all variable declarations that match the given variable name."""
    var_pattern = r'(\w+)\s+' + re.escape(var_name) + r'\s*(;|=|,)'
    return re.findall(var_pattern, code)


def belongs_to_enum(code: str, var_name: str, lang: str) -> bool:
    """see if a given variable name belongs to an enum."""

    enums = find_enums(code, lang)
    enum_types = {enum_name for enum_name, _ in enums}

    var_decl = find_variable_declarations(code, var_name)

    if not var_decl:
        return False

    var_type = var_decl[0][0]
    if var_type in enum_types:
        return True

    return False
