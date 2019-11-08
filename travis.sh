#! /bin/bash

set -ex

if [ "true" = "${INTEGRATION}" ]; then
    export PY3="python${TRAVIS_PYTHON_VERSION}"
    cd integration_test/
    tox -e codegen
    tox -e mypy
    tox -e "${TOXENV}"
else
    tox -e "${TOXENV}"
fi
