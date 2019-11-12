"""Tests of code generation and MyPy type checking."""

import configparser
import os
import os.path
import tokenize
from contextlib import contextmanager

import mypy.api
import pytest
from bravado.client import SwaggerClient

from bravado_types import Config, generate_module
from bravado_types.__main__ import main

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
MYPY_DIR = f"{TESTS_DIR}/mypy"


class Schema:
    def __init__(self, schema_file, name=None, py_file=None, args=None):
        self.schema_file = schema_file
        self.schema_name, _ = os.path.basename(schema_file).split('.')
        self.name = name or self.schema_name.title().replace('_', '')
        self.py_file = py_file or f'{self.schema_name}.py'
        self.pyi_file = f'{py_file}i'
        self.args = None if args is None else (args.split() if args else [])


def _generate_test_classes():
    w = os.walk(MYPY_DIR)
    next(w)  # Skip MYPY_DIR itself
    for path, ds, fs in w:
        ds.clear()  # Don't recurse past first level
        name = os.path.basename(path)
        if 'test.cfg' in fs:
            test_config = configparser.ConfigParser()
            test_config.read(os.path.join(path, 'test.cfg'))
            schemas = []
            for section_name in test_config.sections():
                section = test_config[section_name]
                schemas.append(Schema(schema_file=section['schema_file'],
                                      name=section.get('name'),
                                      py_file=section.get('py_file'),
                                      args=section.get('args')))
        else:
            schemas = [Schema(f) for f in fs if (f.endswith('.json')
                                                 or f.endswith('.yml')
                                                 or f.endswith('.yaml'))]

        generated_modules = {schema.py_file for schema in schemas}
        assert len(generated_modules) == len(schemas)
        modules = [f for f in fs if f.endswith('.py')
                   and f not in generated_modules]
        _generate_test_class(name, path, schemas, modules)


def _generate_test_class(name, path, schemas, modules):
    @classmethod
    def setup_class(cls):
        cls.codegen_errors = {}
        with _chdir(path):
            for schema in schemas:
                for fpath in schema.py_file, schema.pyi_file:
                    if os.path.exists(fpath):
                        os.unlink(fpath)

                try:
                    if schema.args is not None:
                        main(['--url', schema.schema_file,
                              '--name', schema.name,
                              '--path', schema.py_file] + schema.args,
                             exit=False)
                    else:
                        url = f"file://{path}/{schema.schema_file}"
                        swagger_client = SwaggerClient.from_url(url)
                        config = Config(name=schema.name, path=schema.py_file)
                        generate_module(swagger_client, config)
                except Exception as e:
                    cls.codegen_errors[schema.py_file] = e

    @pytest.mark.parametrize('py_file', [schema.py_file for schema in schemas])
    def test_codegen(self, py_file):
        if py_file in self.codegen_errors:
            raise RuntimeError(f"Exception during code generation") \
                from self.codegen_errors[py_file]

        with _chdir(path):
            normal_report, error_report, exit_status = \
                mypy.api.run([f'{py_file}i'])
        assert error_report == ""
        assert normal_report == "Success: no issues found in 1 source file\n"
        assert exit_status == 0

    @pytest.mark.parametrize('module', modules)
    def test_mypy(self, module):
        expected_out = _get_expected_out(f'{path}/{module}')

        with _chdir(path):
            result = mypy.api.run([module])

        out = result[0] or result[1]
        assert expected_out == out.splitlines()

    class_name = f"Test{name.title().replace('_', '')}"
    globals()[class_name] = type(class_name, (), {
        'setup_class': setup_class,
        'test_codegen': test_codegen,
        'test_mypy': test_mypy,
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

    if not expected:
        expected.append("Success: no issues found in 1 source file")
    elif num_errors:
        s = "" if num_errors == 1 else "s"
        expected.append(
            f"Found {num_errors} error{s} in 1 file (checked 1 source file)"
        )

    return expected


_generate_test_classes()
