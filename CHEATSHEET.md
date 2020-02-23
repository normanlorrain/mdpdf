# Cheatsheet 

Instead of Makefile, which is problematic for Windows, and has issues with virtual environements (activating/deactivating, etc).

## Development bootstrap
	python -m venv .venv
	.venv\scripts\activate
	python -m pip install --upgrade pip
	pip install -r requirements.txt
	pip install --editable .


## Packaging 
	python setup.py sdist bdist_wheel
	twine check dist/* 

### test.pypi

	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

	pip install --index-url https://test.pypi.org/simple/ --no-deps mdpdf


	# if that works, then upload to real pypi
	twine upload dist/*
	
## freeze

    pip freeze > requirements.txt

## lint

	pylint mdpdf

