import importlib.machinery
import importlib.util
import inspect
import os
from inspect import signature
from io import StringIO
from typing import List


class StubGenerator:
    """
    This class takes a file as input and generates the corresponding stub file for each type (class) defined inside it at run time.
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

        self._classes: List[type] = [getattr(module, item) for item in dir(module) if inspect.isclass(getattr(module, item))]
        self._stubs_strings: List[str] = []

    def _generate_class_stub(self, clazz: type) -> str:
        """
        Generates the stub string for the given class
        :param clazz: the type to generate stub
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
            if hasattr(element, '__call__'):
                buff.write('\tdef ' + element.__name__ + str(signature(element)) + ':\n')
                if element.__doc__ is not None:
                    buff.write('\t\t"""\n')
                    for line in element.__doc__.split('\n')[1:-1]:
                         buff.write('\t\t' + line.strip().rstrip() + '\n')
                    buff.write('\t\t\"\"\"\n')
                buff.write('\t\t...\n')

        buff.write('\t...\n')

        return buff.getvalue()

    def get_stubs(self) -> List[str]:
        """
        Returns a list containing the generated stub strings
        :return: a list containing the generated stub strings
        :rtype: List[str]
        """
        return self._stubs_strings

    def generate_stubs(self) -> 'StubGenerator':
        """
        Generates the stubs for the classes collected in the input file
        :return: the stub generator
        :rtype StubGenerator
        """
        self._stubs_strings = [self._generate_class_stub(clazz) for clazz in self._classes]
        print(self._stubs_strings[0])
        return  self

    def write_to_file(self):
        """
        Writes the stub files in the same location as the input file
        :return: None
        """
        with open(self._file_path + 'i', mode='w') as f:
            for stub in self._stubs_strings:
                f.write(stub + '\n')
