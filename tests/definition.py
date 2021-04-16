import sys
import numpy as np
import typing as tp
from typing import Any

class A:
    pass

def f_meta(self, c: tp.Callable, i: int, a: A = A(), s: str = 'Hi') -> int:
    """
    docstring
    """
    return 1


class Meta(type):
    def __new__(cls, classname, supers, classdict):
        classdict['f_meta'] = f_meta
        return type.__new__(cls, classname, supers, classdict)


class TestClass(metaclass=Meta):
    def __init__(self, a: np.ndarray, b: Any):
        self._a = a

    def f(self, b: int) -> np.ndarray:
        """
        docstring
        :param b:
        :return:
        """
        return np.array([b])


stub_test_class = """class TestClass(object, metaclass=tests.definition.Meta):
\tdef __init__(self, a: numpy.ndarray, b: typing.Any):
\t\t...
\tdef f(self, b: int) -> numpy.ndarray:
\t\t\"\"\"
\t\tdocstring
\t\t:param b:
\t\t:return:
\t\t\"\"\"
\t\t...
\tdef f_meta(self, c: typing.Callable, i: int, a: tests.definition.A, s: str = 'Hi') -> int:
\t\t\"\"\"
\t\tdocstring
\t\t\"\"\"
\t\t...
\t...\n"""

stub_meta_class = """class Meta(type, metaclass=type):
	...
"""

stub_f_meta = """def f_meta(self, c: typing.Callable, i: int, a: tests.definition.A, s: str = 'Hi') -> int:
\t\"\"\"
\tdocstring
\t\"\"\"
\t...
"""

stub_generic_f_meta = """stub_f_meta: str
"""

stub_lambda = """def lam(x):
	...
"""

lam = lambda x: x