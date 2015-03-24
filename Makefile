help:
	@echo 'Makefile for raspberry client				'
	@echo '												'
	@echo 'Usage:										'
	@echo '   make requirements	install requirements	'

requirements:
	pip install -q -r requirements.txt -i https://pypi.python.org/simple
