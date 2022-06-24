# Cheatsheet 

Instead of Makefile, which is problematic for Windows, and has issues with virtual environements (activating/deactivating, etc).

## Development bootstrap
	python -m venv .venv
	.venv\scripts\activate
	python -m pip install --upgrade pip
	pip install -r requirements.txt
	pip install --editable .

## Testing
	pytest
### verbose tests (stdout/stderr)	
	pytest -s 


## Packaging 
	python -m build
	twine check dist/* 

### test.pypi
	twine upload --repository testpypi dist/*
	python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple your-package

### pypi for real
	# if above tests work, then upload to real pypi
	twine upload dist/*
	
## freeze

    pip freeze > requirements.txt

## lint
	pylint mdpdf

