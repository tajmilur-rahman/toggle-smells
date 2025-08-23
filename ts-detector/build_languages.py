from tree_sitter import Language
import os

os.environ["CC"] = "cc"
os.environ["CFLAGS"] = "-std=c11"

Language.build_library(
    'build/my-languages.so',
    [
        'tree-sitter-python',
        'tree-sitter-java',
        'tree-sitter-cpp',
        'tree-sitter-c-sharp',
        'tree-sitter-go',
    ]
)

print(" Tree-sitter language library built successfully!")