import os.path

import pytest

from stub_generator.stub_generator import StubGenerator
from tests.definition import get_test_class, stub_test_class


def test_constructor():
    with pytest.raises(FileNotFoundError):
        StubGenerator('./fdefinition.py')


def test_generate_class_stub():
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'definition.py')
    generator = StubGenerator(file_path)
    generated_stub = generator._generate_class_stub(get_test_class())
    assert generated_stub == stub_test_class

