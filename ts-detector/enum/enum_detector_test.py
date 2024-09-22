import unittest

from enum_detector import *


class TestEnumDetection(unittest.TestCase):

    def test_enum_in_cpp(self):
        code_cpp = '''
        enum Color { RED, GREEN, BLUE };
        Color myColor = RED;
        '''
        print(type(code_cpp))
        result = belongs_to_enum(code_cpp, "myColor", "c++")
        self.assertTrue(result, "Failed to detect that myColor is an enum in C++")

    def test_enum_in_go(self):
        code_go = '''
        type Color int
        const (
            Red Color = iota
            Green
            Blue
        )
        var myColor Color
        '''
        result = belongs_to_enum(code_go, "myColor", "go")
        print(result)
        self.assertTrue(result, "Failed to detect that myColor is an enum in Go")

    def test_enum_in_python(self):
        code_python = '''
        from enum import Enum
        class Color(Enum):
            RED = 1
            GREEN = 2
            BLUE = 3
        my_color = Color.RED
        '''
        result = belongs_to_enum(code_python, "my_color", "python")
        self.assertTrue(result, "Failed to detect that my_color is an enum in Python")

    def test_enum_in_java(self):
        code_java = '''
        public enum Level { LOW, MEDIUM, HIGH };
        Level myLevel = Level.HIGH;
        '''
        result = belongs_to_enum(code_java, "myLevel", "java")
        self.assertTrue(result, "Failed to detect that myLevel is an enum in Java")

    def test_variable_not_enum(self):
        code_cpp = '''
        int someVar = 10;
        '''
        result = belongs_to_enum(code_cpp, "someVar", "c++")
        self.assertFalse(result, "Incorrectly detected someVar as an enum")

    def test_variable_not_found(self):
        code_java = '''
        public enum Level { LOW, MEDIUM, HIGH };
        Level anotherVar = Level.LOW;
        '''
        result = belongs_to_enum(code_java, "nonexistentVar", "java")
        self.assertFalse(result, "Incorrectly found a nonexistent variable")


if __name__ == '__main__':
    unittest.main()
