.PHONY: clean-pyc clean-build docs clean

help:
	@echo "clean - remove all build, test, coverage and Python artifacts."
	@echo "clean-build - remove build artifacts."
	@echo "clean-pyc - remove Python file artifacts."
	@echo "bump - bumps the version."
	@echo "test-register - register the project at TestPyPI."
	@echo "register - register the project at PyPI."
	@echo "test-upload - package and upload a releaes to TestPyPI."
	@echo "upload - package and upload a upload to PyPI."
	@echo "dist - package."
	@echo "install - install the package to the active Python's site-packages."

clean: clean-build clean-pyc 

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf .eggs/
	find . -name '*.egg-info' -exec rm -rf {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

bump:
	python -m scripts.bump

dist: clean
	python setup.py sdist
	python setup.py bdist_wheel

test-register:
	python setup.py register -r test

register:
	python setup.py register

test-upload:
	twine upload -r test $(wildcard dist/*)

upload:
	twine upload $(wildcard dist/*)

install:
	python setup.py install
