import importlib.machinery
import importlib.util
import inspect
import os
import pkgutil
from inspect import signature
from io import StringIO
from types import ModuleType
from typing import List, Callable, Any


class StubGenerator:
    """
    This class takes a file as input and generates the corresponding stub file for each types (generic variables, functions, classes)
    defined inside it at run time.
    This means that the file is not statically parsed, but it is executed and
    then the types are dynamically created and analyzed to produce the stub file.
    """
    def __init__(self, file_path: str):
        self._file_path: str = file_path
        if not os.path.exists(self._file_path):
            raise FileNotFoundError
        loader = importlib.machinery.SourceFileLoader('imported', self._file_path)
        spec = importlib.util.spec_from_loader(loader.name, loader)
        module = importlib.util.module_from_spec(spec)
        loader.exec_module(module)
        self._module = module

        self._members: List[str] = [item for item in module.__dict__.keys() if not item.startswith('__')]
        self._modules: List[ModuleType] = [getattr(module, item) for item in module.__dict__.keys() if inspect.ismodule(getattr(module, item))]
        self._stubs_strings: List[str] = []

    def _generate_class_stub(self, clazz: type) -> str:
        """
        Generates the stub string for the given class
        :param clazz: the class to generate stub
        :type clazz: type
        :return: the str which contains the stub
        :rtype: str
        """
        buff = StringIO()

        # Class prototype
        buff.write('class ' + clazz.__name__.split('.')[-1] + '(')

        # Add super classes
        for c in clazz.__bases__:
            buff.write(c.__name__ + ', ')

        # Add metaclass
        buff.write('metaclass=' + clazz.__class__.__name__ + '):\n')

        for key, element in clazz.__dict__.items():
            if inspect.isfunction(element):
                buff.write(self._generate_function_stub(element, indentation='\t'))

        buff.write('\t...\n')

        return buff.getvalue()

    def _generate_function_stub(self, func: Callable, indentation: str = '') -> str:
        """
        Generates the stub string for the given function
        :param func: the function to generate stub
        :type func: Callable
        :param indentation: the string used to correctly align the function stub
        :return: the str which contains the stub
        :rtype: str
        """
        buff = StringIO()
        buff.write(indentation + 'def ' + func.__name__ + str(signature(func)) + ':\n')
        if func.__doc__ is not None:
            buff.write(indentation + '\t"""\n')
            for line in func.__doc__.split('\n')[1:-1]:
                buff.write(indentation + '\t' + line.strip().rstrip() + '\n')
            buff.write(indentation + '\t\"\"\"\n')
        buff.write(indentation + '\t...\n')
        return buff.getvalue()

    def _generate_generic_stub(self, element_name: str, element: Any) -> str:
        """
        Generates the stub for a generic variable
        :param element_name: the name of the element
        :type element_name: str
        :param element: the element
        :type element: Any
        :return: the stub as a string
        :rtype: str
        """
        return '{0}: {1}\n'.format(element_name, type(element).__name__)

    def get_stubs(self) -> List[str]:
        """
        Returns a list containing the generated stub strings
        :return: a list containing the generated stub strings
        :rtype: List[str]
        """
        return self._stubs_strings

    def generate_stubs(self) -> 'StubGenerator':
        """
        Generates the stubs for the types collected in the input file
        :return: the stub generator
        :rtype StubGenerator
        """
        for member_name in self._members:
            attr = getattr(self._module, member_name)
            if inspect.isclass(attr):
                self._stubs_strings.append(self._generate_class_stub(attr))
            elif inspect.isfunction(attr):
                self._stubs_strings.append(self._generate_function_stub(attr))
            elif not inspect.ismodule(attr):
                self._stubs_strings.append(self._generate_generic_stub(member_name, attr))

        return self

    def write_to_file(self):
        """
        Writes the stub files in the same location as the input file
        :return: None
        """
        with open(self._file_path + 'i', mode='w') as f:
            for module in self._modules:
                f.write('import ' + module.__name__ + '\n')
            f.write('\n')
            for stub in self._stubs_strings:
                f.write(stub + '\n')
