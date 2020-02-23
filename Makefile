# Makefile for managing development
# On Windows, this is flakey, and I may abandon it, but to get started, 
# install make with "chocolatey" (https://chocolatey.org/install)
#   choco install make

.DEFAULT_GOAL := package
.PHONY: package publish package coverage test lint docs venv venv-clean
PROJ_SLUG = mdpdf

ifeq ($(OS),Windows_NT)
	REMOVE=rmdir /s /q
else
	REMOVE=rm -rf
endif


freeze:
	pip freeze > requirements.txt

lint:
	pylint $(PROJ_SLUG)

test: lint
	py.test --cov-report term --cov=$(PROJ_SLUG) tests/

quicktest:
	py.test --cov-report term --cov=$(PROJ_SLUG) tests/

coverage: lint
	py.test --cov-report html --cov=$(PROJ_SLUG) tests/

package: clean 
	python setup.py sdist bdist_wheel
	twine check  dist/* 

publish: package
	twine upload dist/*

testpublish: package 
	python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

clean :
	-$(REMOVE) dist
	-$(REMOVE) build
	-$(REMOVE) mdpdf.egg-info

venv-clean :
	where python
	-deactivate
	where python
	
#	$(REMOVE) .venv

venv:
	python -m venv .venv

bootstrap:
	.venv\scripts\activate
	python -m pip install --upgrade pip
	pip install -r requirements.txt
	pip install --editable .
