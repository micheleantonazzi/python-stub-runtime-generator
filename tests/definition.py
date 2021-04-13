import sys

import numpy as np

def get_test_class():
    def f_meta(self, a: int, s: str = 'Hi') -> int:
        return a + 1

    class Meta(type):
        def __new__(cls, classname, supers, classdict):
            classdict['f_meta'] = f_meta
            return type.__new__(cls, classname, supers, classdict)

    class TestClass(metaclass=Meta):
        def __init__(self, a: np.ndarray):
            self._a = a

        def f(self, b: int) -> np.ndarray:
            """
            ciao
            :param b:
            :return:
            """
            return np.array([b])

    return TestClass

if sys.version_info[0] == 3.6:
    stub_test_class = """class TestClass(object, metaclass=Meta):
    \tdef __init__(self, a:numpy.ndarray):
    \t\t...
    \tdef f(self, b:int) -> numpy.ndarray:
    \t\t\"\"\"
    \t\tciao
    \t\t:param b:
    \t\t:return:
    \t\t\"\"\"
    \t\t...
    \tdef f_meta(self, a:int, s:str = 'Hi') -> int:
    \t\t...\n"""
else:
    stub_test_class = """class TestClass(object, metaclass=Meta):
    \tdef __init__(self, a: numpy.ndarray):
    \t\t...
    \tdef f(self, b: int) -> numpy.ndarray:
    \t\t\"\"\"
    \t\tciao
    \t\t:param b:
    \t\t:return:
    \t\t\"\"\"
    \t\t...
    \tdef f_meta(self, a: int, s: str = 'Hi') -> int:
    \t\t...\n"""