"""Tests of code generation and MyPy type checking."""

import os
import os.path
import tokenize
from contextlib import contextmanager

import mypy.api
import pytest
from bravado.client import SwaggerClient

from bravado_types import RenderConfig, generate_module

TESTS_DIR = os.path.abspath(os.path.dirname(__file__))
PETSTORE_DIR = f"{TESTS_DIR}/petstore"
PY_FILE = f"{PETSTORE_DIR}/petstore.py"
PYI_FILE = f"{PETSTORE_DIR}/petstore.pyi"


@contextmanager
def chdir(path):
    prev_wd = os.path.abspath(os.getcwd())
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_wd)


@pytest.fixture(scope="module")
def swagger_client():
    return SwaggerClient.from_url(f"file://{PETSTORE_DIR}/schema.json")


@pytest.fixture(scope="module", autouse=True)
def generate_petstore_module(swagger_client):
    for path in PY_FILE, PYI_FILE:
        if os.path.exists(path):
            os.unlink(path)

    render_config = RenderConfig(name="PetStore", path=PY_FILE)
    generate_module(swagger_client, render_config)


@pytest.mark.parametrize("example", ["example.py", "bad_example.py"])
def test_with_mypy(example):
    with chdir(PETSTORE_DIR):
        result = mypy.api.run([example])
    out = result[0] or result[1]
    expected_out = _get_expected_out(example)
    assert expected_out == out.splitlines()


def _get_expected_out(filename):
    """Convert module comments to expected MyPy output."""
    expected = []
    num_errors = 0

    prev = None
    with open(f"{PETSTORE_DIR}/{filename}", "rb") as f:
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
