from tree_sitter import Language, Parser

LANGUAGE_SO = "build/my-languages.so"
LANGUAGES = {
    "python": "python",
    "java": "java",
    "cpp": "cpp",
    "c++": "cpp",
    "go": "go",
    "csharp": "c_sharp" 
}
LANG_OBJS = {lang: Language(LANGUAGE_SO, lib) for lang, lib in LANGUAGES.items()}

def extract_functions(source_code, lang_name):
    parser = Parser()
    parser.set_language(LANG_OBJS[lang_name])
    tree = parser.parse(bytes(source_code, "utf8"))
    root = tree.root_node
    funcs = []

    def visit(node):
        if node.type in ("function_definition", "method_definition", "method_declaration"):
            name_node = node.child_by_field_name("name")
            if name_node:
                name = source_code[name_node.start_byte:name_node.end_byte]
                funcs.append({
                    "name": name,
                    "start_byte": node.start_byte,
                    "end_byte": node.end_byte
                })
        for child in node.children:
            visit(child)

    visit(root)
    return funcs

def match_toggle_usage(source_code, functions, toggle_name):
    results = {}
    for fn in functions:
        body = source_code[fn["start_byte"]:fn["end_byte"]]
        count = body.count(toggle_name)
        if count > 0:
            results[fn["name"]] = count
    return results