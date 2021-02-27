.PHONY: build

init:
	pyenv install -sf 3.9.0
	pyenv local 3.9.0
	pip install --exists-action i -qqq pipenv

build:
	rm -fr dist/ build/
	pipenv --python 3.9 install --dev
	pipenv run python setup.py bdist_wheel

