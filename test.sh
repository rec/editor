#!/bin/bash

set -eux

mypy editor
isort editor test_editor.py
black editor test_editor.py
ruff check --fix editor test_editor.py
coverage run $(which pytest)
coverage html
