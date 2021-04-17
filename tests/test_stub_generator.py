import os.path
import pytest
import filecmp

from stub_generator.stub_generator import StubGenerator
from tests.definition import TestClass, stub_test_class, stub_meta_class, Meta, f_meta, stub_f_meta, stub_generic_f_meta, lam, stub_lambda


def test_constructor():
    with pytest.raises(FileNotFoundError):
        StubGenerator('./fdefinition.py')

    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'definition.py')
    generator = StubGenerator(file_path, ['error']).generate_stubs()
    assert len(generator.get_stubs()) == 10
    generator = StubGenerator(file_path, ['f_meta']).generate_stubs()
    assert len(generator.get_stubs()) == 10



def test_generate_function_stub():
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'definition.py')
    generator = StubGenerator(file_path)
    generated_stub_f_meta = generator._generate_function_stub(f_meta.__name__, f_meta)
    generate_stub_lambda = generator._generate_function_stub('lam', lam)
    assert generated_stub_f_meta == stub_f_meta
    assert generate_stub_lambda == stub_lambda


def test_generate_class_stub():
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'definition.py')
    generator = StubGenerator(file_path)
    generated_stub_test_class = generator._generate_class_stub(TestClass.__name__, TestClass)
    generated_stub_meta_class = generator._generate_class_stub(Meta.__name__, Meta)

    assert generated_stub_test_class == stub_test_class
    assert generated_stub_meta_class == stub_meta_class


def test_generate_generic_stub():
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'definition.py')
    generator = StubGenerator(file_path)
    generated_stub_generic = generator._generate_generic_stub('stub_f_meta', stub_f_meta)
    assert generated_stub_generic == stub_generic_f_meta


def test_generate_stubs_strings():
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'definition.py')
    generator = StubGenerator(file_path, ['f_meta'])
    generator.generate_stubs().write_to_file()
    try:
        os.path.exists(file_path + 'i')
    except FileNotFoundError:
        assert False

    assert len(generator.get_stubs()) == 10

def test_write_to_file():
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'definition.py')
    generator = StubGenerator(file_path, ['f_meta'])
    generator.generate_stubs().write_to_file()
    assert filecmp.cmp(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'definition.pyi'), os.path.join(os.path.dirname(os.path.abspath(__file__)), 'definition_final.test'))

