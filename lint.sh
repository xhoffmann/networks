#!/usr/bin/env bash

set -e
set -x

black networks
mypy networks
flake8 networks --ignore=E203,E501,W503 --max-line-length=88 --max-doc-length=72 --max-complexity=15 --select=C,E,F,W,T4
pydocstyle networks --convention=google
