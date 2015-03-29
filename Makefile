help:
	@echo 'Makefile for raspberry client				'
	@echo '												'
	@echo 'Usage:										'
	@echo '   make requirements	install requirements	'
	@echo '   make deamon set supervisor cfg'

requirements:
	pip install -q -r requirements.txt -i https://pypi.python.org/simple

deamon:
	echo 'supervisord' | tee -a /etc/rc.local
	cp supervisor/client.ini /etc/supervisor.d/
