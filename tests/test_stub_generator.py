import os.path

import numpy.lib.format
import pytest

from stub_generator.stub_generator import StubGenerator
from tests.definition import TestClass, stub_test_class


def test_constructor():
    with pytest.raises(FileNotFoundError):
        StubGenerator('./fdefinition.py')


def test_generate_class_stub():
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'definition.py')
    generator = StubGenerator(file_path)
    generated_stub = generator._generate_class_stub(TestClass)
    assert generated_stub == stub_test_class

def test_generate_stubs_strings():
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'definition.py')
    generator = StubGenerator(file_path)
    generator.generate_stubs()
