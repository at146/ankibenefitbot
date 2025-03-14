#!/bin/sh

set -e
set -x

mypy bot
ruff check bot
ruff format bot --check
