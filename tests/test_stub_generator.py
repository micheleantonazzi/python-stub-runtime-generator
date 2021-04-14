import os.path
import pytest

from stub_generator.stub_generator import StubGenerator
from tests.definition import TestClass, stub_test_class, stub_meta_class, Meta, f_meta, stub_f_meta


def test_constructor():
    with pytest.raises(FileNotFoundError):
        StubGenerator('./fdefinition.py')

def test_generate_function_stub():
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'definition.py')
    generator = StubGenerator(file_path)
    generated_stub_f_meta = generator._generate_function_stub(f_meta)
    assert generated_stub_f_meta == stub_f_meta


def test_generate_class_stub():
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'definition.py')
    generator = StubGenerator(file_path)
    generated_stub_test_class = generator._generate_class_stub(TestClass)
    generated_stub_meta_class = generator._generate_class_stub(Meta)

    assert generated_stub_test_class == stub_test_class
    assert generated_stub_meta_class == stub_meta_class


def test_generate_stubs_strings():
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'definition.py')
    generator = StubGenerator(file_path)
    generator.generate_stubs().write_to_file()
    try:
        os.path.exists(file_path + 'i')
    except FileNotFoundError:
        assert False
