help:
	@echo 'Makefile for raspberry client                                '
	@echo '												                '
	@echo 'Usage:										                '
	@echo '   make requirements	    install requirements	            '
	@echo '   make cfg              cp supervisor cfg                   '
	@echo '   make supervisor       set up supervisor                   '
	@echo '   make encrypt          encrypt settings                    '
	@echo '   make decrypt          decrypt settings                    '

requirements:
	pip install -q -r requirements.txt -i https://pypi.python.org/simple

cfg:
	cp supervisor/client.ini /etc/supervisor.d/

supervisor:
	cp supervisor/supervisord /etc/init.d/
	chmod +x /etc/init.d/supervisord
	update-rc.d supervisord defaults

encrypt:
	ansible-vault encrypt settings.yml

decrypt:
	ansible-vault decrypt settings.yml
