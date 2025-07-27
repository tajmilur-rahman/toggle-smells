from tree_sitter import Language
import os

os.environ["CC"] = "cc"
os.environ["CFLAGS"] = "-std=c11"

Language.build_library(
    'build/my-languages.so',
    [
        'tree-sitter-python',
        'tree-sitter-java',
        # 'tree-sitter-cpp',   Temporarily comment this
        'tree-sitter-c-sharp',
        'tree-sitter-go',
        'tree-sitter-c',
    ]
)

print(" Tree-sitter language library built successfully (without C++)!")