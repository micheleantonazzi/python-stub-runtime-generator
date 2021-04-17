# Python stub runtime generator
![](https://github.com/micheleantonazzi/python-stub-runtime-generator/workflows/Build/badge.svg?branch=main)
[![pypi package](https://img.shields.io/pypi/v/stub-generator.svg)](https://pypi.org/project/stub-generator/)
[![](https://sonarcloud.io/api/project_badges/measure?project=micheleantonazzi_python-stub-runtime-generator&metric=coverage)](https://sonarcloud.io/dashboard/index/micheleantonazzi_python-stub-runtime-generator)



[![](https://sonarcloud.io/api/project_badges/measure?project=micheleantonazzi_python-stub-runtime-generator&metric=alert_status)](https://sonarcloud.io/dashboard/index/micheleantonazzi_python-stub-runtime-generator)
[![](https://sonarcloud.io/api/project_badges/measure?project=micheleantonazzi_python-stub-runtime-generator&metric=sqale_rating)](https://sonarcloud.io/dashboard/index/micheleantonazzi_python-stub-runtime-generator)
[![](https://sonarcloud.io/api/project_badges/measure?project=micheleantonazzi_python-stub-runtime-generator&metric=reliability_rating)](https://sonarcloud.io/dashboard/index/micheleantonazzi_python-stub-runtime-generator)
[![](https://sonarcloud.io/api/project_badges/measure?project=micheleantonazzi_python-stub-runtime-generator&metric=security_rating)](https://sonarcloud.io/dashboard/index/micheleantonazzi_python-stub-runtime-generator)
[![](https://sonarcloud.io/api/project_badges/measure?project=micheleantonazzi_python-stub-runtime-generator&metric=vulnerabilities)](https://sonarcloud.io/dashboard/index/micheleantonazzi_python-stub-runtime-generator)

This utility package generates Python stub files at run time to enhance the autocomplete capabilities of your favorite Python IDE.

Python is a dynamically typed language: the Python interpreter does type checking only when the code is run. This means that the type of a variable is allowed to change over its lifetime. 
However, Python 3.x syntax introduces *type hints*, which makes it possible to statically checking of Python code. 
Despite this mechanism, Python doesn't work like other statically typed languages. 
In fact, *type hints* don't cause the type enforcing, but it provides only suggestions to prevent common mistakes.
The most famous Python IDEs help programmers providing an autocomplete system, which suggests the types of a variable, the method of a class, the parameters of a method and so on.
This makes coding faster and easier. It analyses statically the Python files and, with the help of *type hints*, gives to the coder a lot of useful information to improve its activity.
However, Python implements the *metaprogramming* paradigm.
The term *metaprogramming* refers to the potential for a program to have knowledge of or manipulate itself.
In other words, Python allows generating code at run time using the metaclasses.
This represents an obstacle to autocomplete systems: they cannot suggest what is defined during the code execution.
To solve this issue, it is possible to use a *stub file*,
that a skeleton of the public interface of the library, including classes, variables and functions, and their types.
This utility automatically creates stub files loading the Python code and analyzing it dynamically.

## How it works
The main object is called StubGenerator. It takes a Python file path and generates the corresponding stub file in the same directory. 

**NB:** annotate as much as possible your Python file to improve the stub file quality. Use *doc-strings* and *type hints*.

To produce a stub file, run this code 

```python
StubGenerator(file_path='*.py', members_from_other_modules=['member_defined_in_other_module',...]).generate_stubs().write_to_file()
```

```StubGenerator(file_path='*.py', members_from_other_modules=['member_defined in other_module',...]).generate_stubs().write_to_file()```. The StubGenerator object produces the stub file of the given file and save it in the same path. By default, only members defined in that file are considered, the others are ignored. It is possible to produce the stub for a member defined in another file, just use the second parameter of the constructor.

For example, if you have a Python file like this:

```python
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
. its name 

s = 'string'

lam = lambda x: x
```

This module produces the the following stub file:

```python
import sys
import numpy
import typing

class A(object, metaclass=type):
	...

def f_meta(self, c: typing.Callable, i: int, a: A, s: str = 'Hi') -> int:
	"""
	docstring
	"""
	...

class Meta(type, metaclass=type):
	...

class TestClass(object, metaclass=Meta):
	def __init__(self, a: numpy.ndarray, b: typing.Any):
		...
	def f(self, b: int) -> numpy.ndarray:
		"""
		docstring
		:param b:
		:return:
		"""
		...
	def f_meta(self, c: typing.Callable, i: int, a: A, s: str = 'Hi') -> int:
		"""
		docstring
		"""
		...
	...

s: str

def lam(x):
	...
```

## Tips

To use this module successfully, you need to change your code style a little, following these tips:

* *StubGenerator* considers only the types that are defined in the input file. For example, the line ```MyException = Exception``` is ignored, because the type *MyExcpetion* is another way to call *Exception* type, which is defined in another file. This issues can be easily overcome passing 'MyException' to StubGenerator constructor:

  ```python
  StubGenerator(file_path='*.py', members_from_other_modules=['MyException']).generate_stubs().write_to_file()
  ```

  or defining a new type:

  ```python
  class MyException(Exception):
  	pass
  ```

* the default parameters of a function are ignored if they are objects other than strings, integers, floats, etc. For example, for a function like this ```def f(s = 'Hi', a = A()): pass``` the output will be ```def f(s = 'Hi', a): pass```. This is an error for the Python syntax, just invert the parameter.