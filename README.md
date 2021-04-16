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
However, Python 3.x syntax introduces *type hints*, which make possible to statically checking of Python code. 
Despite this mechanism, Python doesn't work like other statically typed languages. 
In fact, *type hints* don't cause the type enforcing, but it provides only suggestions to prevent common mistakes.
The most famous Python IDE help programmers providing an autocomplete system, which suggest the types of a variable, the method of a class, the parameters of a method and so on.
This make coding faster and easier. It analyses statically the Python files and, with the help of *type hints*, gives to the coder a lot of useful information to improve its activity.
However, Python implements the *metaprogramming* paradigm.
The term *metaprogramming* refers to the potential for a program to have knowledge of or manipulate itself.
In other words, Python allows generating code at run time using the metaclasses.
This represents an obstacle to autocomplete systems: they cannot suggest what is defined during the code execution.
To solve this issue, it is possible use a *stub file*,
that a skeleton of the public interface of the library, including classes, variables and functions, and their types.
This utility automatically creates stub file loading the Python code and analysing it dynamically.

## How it works
The main object is called StubGenerator.
It takes a Python file path and generates the corresponding stub file in the same directory.

