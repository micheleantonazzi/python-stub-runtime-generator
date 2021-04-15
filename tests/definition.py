import sys
import numpy as np
import typing as tp

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
    def __init__(self, a: np.ndarray):
        self._a = a

    def f(self, b: int) -> str:
        """
        docstring
        :param b:
        :return:
        """
        return 'Hi'


stub_test_class = """class TestClass(object, metaclass=tests.definition.Meta):
\tdef __init__(self, a: numpy.ndarray):
\t\t...
\tdef f(self, b: int) -> str:
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

lam = lambda x: x