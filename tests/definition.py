import sys

import numpy as np


def f_meta(self, a: int, s: str = 'Hi') -> int:
    """
    docstring
    """
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
        docstring
        :param b:
        :return:
        """
        return np.array([b])


if (3, 6) <= sys.version_info < (3, 7):
    stub_test_class = """class TestClass(object, metaclass=Meta):
\tdef __init__(self, a:numpy.ndarray):
\t\t...
\tdef f(self, b:int) -> numpy.ndarray:
\t\t\"\"\"
\t\tdocstring
\t\t:param b:
\t\t:return:
\t\t\"\"\"
\t\t...
\tdef f_meta(self, a:int, s:str='Hi') -> int:
\t\t\"\"\"
\t\tdocstring
\t\t\"\"\"
\t\t...
\t...\n"""
else:
    stub_test_class = """class TestClass(object, metaclass=Meta):
\tdef __init__(self, a: numpy.ndarray):
\t\t...
\tdef f(self, b: int) -> numpy.ndarray:
\t\t\"\"\"
\t\tdocstring
\t\t:param b:
\t\t:return:
\t\t\"\"\"
\t\t...
\tdef f_meta(self, a: int, s: str = 'Hi') -> int:
\t\t\"\"\"
\t\tdocstring
\t\t\"\"\"
\t\t...
\t...\n"""

stub_meta_class = """class Meta(type, metaclass=type):
	...
"""

stub_f_meta = """def f_meta(self, a: int, s: str = 'Hi') -> int:
\t\"\"\"
\tdocstring
\t\"\"\"
\t...
"""