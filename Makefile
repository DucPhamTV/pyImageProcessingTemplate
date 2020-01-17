.PHONY: venv

PACKAGE_NAME=py_image
VENV_NAME?=venv
PYTHON=${VENV_NAME}/bin/python3
PIP=${VENV_NAME}/bin/pip3

.DEFAULT: help

help:
	@echo "To be defined"

prepare-dev:
	python3 -m pip install virtualenv
	make venv

venv: requirements.txt
	python3 -m venv $(VENV_NAME)
	${PIP} install -r requirements.txt

lint: | venv
	${PYTHON} -m pylint $(PACKAGE_NAME)/
	${PYTHON} -m mypy

clean:
	find . -name '*.pyc' -exec rm --force {} +
	rm -rf $(VENV_NAME) *.eggs *.egg-info dist build docs/_build .cache
