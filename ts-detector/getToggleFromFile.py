import os
import re

# Define the regexes dictionary for different languages
regexes = {
    'python': {
        'declare': r'^\s*(?P<toggle>\w+)\s*(?:\:\s*(?P<type>[^\s=]+))?\s*=\s*',
        'capital_identifiers': r'(?P<toggle>[A-Z][A-Z0-9_-]{2,})',
        'dict_keys': r'[{,]\s*(?P<toggle>(?:[\'\"][^\'\"]*[\'\"]|[^:]+?))\s*:'
    },
    'csharp': {
        'declare': (
            r'^\s*(public|protected\s+internal|protected|internal|private\s+protected|private)\s+'
            r'(?:static\s+|const\s+|readonly\s+|volatile\s+)*'
            r'(?P<type>\w+(?:\s*<[^>]+>)?)\s+'
            r'(?P<toggle>\w+)\s*'
            r'(?=\s*(=|;|\[))'
        ),
        'capital_identifiers': r'(?P<toggle>[A-Z][A-Z0-9_-]{2,})',
        'dict_keys': r'[{,]\s*(?P<toggle>(?:@"[^"]*"|"[^"]*"|\'[^\']*\'|[^,\s]+?))\s*,'
    },
    'java': {
        'declare': (
            r'^\s*(public|protected|private)\s+'
            r'(?:static\s+|final\s+|volatile\s+|transient\s+)*'
            r'(?P<type>\w+(?:\s*<[^>]+>)?)\s+'
            r'(?P<toggle>\w+)\s*'
            r'(?=\s*(=|;|\[))'
        ),
        'capital_identifiers': r'(?P<toggle>[A-Z][A-Z0-9_-]{2,})',
        'dict_keys': r'\bput\s*\(\s*(?P<toggle>"[^"]*"|\'[^\']*\'|[^,\s]+?)\s*,'
    },
    'golang': {
        'declare': (
            r'^\s*(?:var\s+(?P<toggle>\w+)\s*(?:\s+(?P<type>[^\s=]+))?\s*(?:=\s*.*)?|'
            r'(?P<toggle2>\w+)\s*(?:\s+(?P<type2>[^\s=]+))?\s*:=\s*.*)'
        ),
        'capital_identifiers': r'(?P<toggle>[A-Z][A-Z0-9_-]{2,})',
        'dict_keys': r'[{,]\s*(?P<toggle>(?:`[^`]*`|"[^"]*"|\'[^\']*\'|[\w.]+?))\s*:'
    },
    'cpp': {
        'declare': (
            r'^\s*(?:(?:const|static|volatile|extern|mutable)\s+)*'
            r'(?P<type>(?:[\w:]+)(?:\s*<[^>;]+>)?'
            r'(?:\s*::\s*[\w:]+)*(?:\s*[\*&])?)\s+'
            r'(?P<toggle>\w+)\s*'
            r'(?=\s*(=|;|\[))'
        ),
        'capital_identifiers': r'(?P<toggle>[A-Z][A-Z0-9_-]{2,})',
        'dict_keys': r'[{,]\s*(?P<toggle>(?:"[^"]*"|\'[^\']*\'|[^,\s]+?))\s*,',
        'toggle_names': r'{\s*Toggle::(?P<toggle>\w+),'
    }
}

# Function to apply regexes and extract toggles from file content based on language
def apply_regexes(file_content, language):
    toggles = set()  # Use a set to avoid duplicates

    # Get the regexes for the current language
    patterns = regexes.get(language)

    if patterns:
        # Apply each regex and collect results
        for pattern in patterns.values():
            compiled_pattern = re.compile(pattern)
            matches = compiled_pattern.finditer(file_content)
            for match in matches:
                toggle = match.group('toggle')
                toggles.add(toggle)

    return toggles

# Determine the language based on file extension
def get_language_from_extension(file_path):
    if file_path.endswith('.py'):
        return 'python'
    elif file_path.endswith('.cs'):
        return 'csharp'
    elif file_path.endswith('.java'):
        return 'java'
    elif file_path.endswith('.go'):
        return 'golang'
    elif file_path.endswith('.cpp') or file_path.endswith('.cc'):
        return 'cpp'
    return None

# Main function to extract all unique toggles from a directory of config files
def extract_toggles_from_files(config_files_path):
    all_toggles = set()

    for root, _, files in os.walk(config_files_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            language = get_language_from_extension(file_path)

            if language:
                # Read the file content
                with open(file_path, 'r') as file:
                    content = file.read()

                # Extract toggles using the appropriate regexes
                file_toggles = apply_regexes(content, language)
                all_toggles.update(file_toggles)

    return list(all_toggles)  # Convert set to list and return

# Example usage
if __name__ == "__main__":
    config_files_path = "/path/to/your/config/files"  # Replace with the path to your config files
    toggles = extract_toggles_from_files(config_files_path)
    print("Extracted Toggles:", toggles)
