"""Tests of code generation and MyPy type checking."""

import os
import os.path
import tokenize
from contextlib import contextmanager

import mypy.api
import pytest
from bravado.client import SwaggerClient

from bravado_types import RenderConfig, generate_module

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
MYPY_DIR = f"{TESTS_DIR}/mypy"


def _generate_test_classes():
    w = os.walk(MYPY_DIR)
    next(w)  # Skip MYPY_DIR itself
    for path, ds, fs in w:
        ds.clear()  # Don't recurse past first level
        name = os.path.basename(path)
        schemas = [f for f in fs if (f.endswith('.json') or f.endswith('.yml')
                                     or f.endswith('.yaml'))]
        generated_modules = {f.split('.')[0] + '.py' for f in schemas}
        modules = [f for f in fs if f.endswith('.py')
                   and f not in generated_modules]
        _generate_test_class(name, path, schemas, modules)


def _generate_test_class(name, path, schemas, modules):
    @pytest.fixture(scope='class', autouse=True)
    def codegen(self):
        for schema in schemas:
            swagger_client = SwaggerClient.from_url(
                f"file://{path}/{schema}")
            name, ext = schema.split('.')
            py_file = '{}/{}.py'.format(path, name)
            pyi_file = '{}/{}.pyi'.format(path, name)

            for fpath in py_file, pyi_file:
                if os.path.exists(fpath):
                    os.unlink(fpath)

            render_config = RenderConfig(name=name.title(), path=py_file)
            generate_module(swagger_client, render_config)

    @pytest.mark.parametrize('module', modules)
    def test_with_mypy(self, module):
        expected_out = _get_expected_out(f'{path}/{module}')

        with _chdir(path):
            result = mypy.api.run([module])

        out = result[0] or result[1]
        assert expected_out == out.splitlines()

    class_name = f'Test{name.title()}'
    globals()[class_name] = type(class_name, (), {
        'codegen': codegen,
        'test_with_mypy': test_with_mypy,
    })


@contextmanager
def _chdir(path):
    prev_wd = os.path.abspath(os.getcwd())
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_wd)


def _get_expected_out(path):
    """Convert module comments to expected MyPy output."""
    filename = os.path.basename(path)
    expected = []
    num_errors = 0

    prev = None
    with open(path, "rb") as f:
        for token in tokenize.tokenize(f.readline):
            if token.type == tokenize.COMMENT:
                if token.string.startswith("# error:"):
                    num_errors += 1
                if prev:
                    expected.append(f"{filename}:{prev.start[0]}: "
                                    f"{token.string[2:]}")
                else:
                    expected.append(f"{filename}:{token.start[0]}: "
                                    f"{token.string[2:]}")
                    prev = token
            elif token.type != tokenize.NEWLINE:
                prev = None

    if num_errors:
        s = "" if num_errors == 1 else "s"
        expected.append(
            f"Found {num_errors} error{s} in 1 file (checked 1 source file)"
        )

    return expected


_generate_test_classes()
