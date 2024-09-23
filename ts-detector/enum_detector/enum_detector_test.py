import unittest
from enum_detector import *


class TestEnumParsing(unittest.TestCase):

    def test_java_enum(self):
        java_code = """
        public enum Day {
            SUNDAY, MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY
        }
        """
        self.assertTrue(is_enum_member(java_code, "MONDAY", "java"))
        self.assertFalse(is_enum_member(java_code, "BLACK", "java"))

    def test_python_enum(self):
        python_code = """
        from enum import Enum
        class Day(Enum):
            SUNDAY = 1
            MONDAY = 2
        """
        self.assertTrue(is_enum_member(python_code, "MONDAY", "python"))
        self.assertFalse(is_enum_member(python_code, "BLACK", "python"))

    def test_go_enum(self):
        go_code = """
        const (
            SUNDAY = iota
            MONDAY
            TUESDAY
        )
        """
        self.assertTrue(is_enum_member(go_code, "MONDAY", "go"))
        self.assertFalse(is_enum_member(go_code, "BLACK", "go"))

    def test_cpp_enum(self):
        cpp_code = """
        enum Day { SUNDAY, MONDAY, TUESDAY, WEDNESDAY };
        """
        self.assertTrue(is_enum_member(cpp_code, "MONDAY", "cpp"))
        self.assertFalse(is_enum_member(cpp_code, "BLACK", "cpp"))

    def test_csharp_enum(self):
        csharp_code = """
        public enum Day {
            SUNDAY, MONDAY, TUESDAY, WEDNESDAY
        }
        """
        self.assertTrue(is_enum_member(csharp_code, "MONDAY", "csharp"))
        self.assertFalse(is_enum_member(csharp_code, "BLACK", "csharp"))

    def test_c_enum(self):
        c_code = """
        enum Day { SUNDAY, MONDAY, TUESDAY, WEDNESDAY };
        """
        self.assertTrue(is_enum_member(c_code, "MONDAY", "c"))
        self.assertFalse(is_enum_member(c_code, "BLACK", "c"))


if __name__ == "__main__":
    unittest.main()
