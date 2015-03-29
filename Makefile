help:
	@echo 'Makefile for raspberry client				'
	@echo '												'
	@echo 'Usage:										'
	@echo '   make requirements	install requirements	'
	@echo '   make build set supervisor cfg'
	@echo '   make supervisord set supervisord start with system'

requirements:
	pip install -q -r requirements.txt -i https://pypi.python.org/simple

build:
	cp supervisor/client.ini /etc/supervisor.d/

supervisord:
	cp supervisor/supervisord /etc/init.d/
	update-rc.d supervisord defaults
