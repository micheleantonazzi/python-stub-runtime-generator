from typing import Type
from io import StringIO
from inspect import signature
import os


class StubGenerator:
    """
    This class takes a file as input and generates the corresponding stub file at run time.
    This means that the file is not statically parsed, but it is executed and
    then the types are created and analyzed to produce the stub file.
    """
    def __init__(self, file_path: str):
        self._file_path: str = file_path
        if not os.path.exists(self._file_path):
            raise FileNotFoundError
        for item in dir(self._file_path):
            pass

    def _generate_class_stub(self, clazz: type) -> str:
        """
        Generates the stub string for the given class
        :param clazz: the type to generate stub
        :return: the str which contains the stub
        :rtype: str
        """
        buff = StringIO()

        # Class prototype
        buff.write('class ' + clazz.__name__ + '(')

        # Add super classes
        for c in clazz.mro()[1:]:
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

        return buff.getvalue()
