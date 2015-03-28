import yaml
import logging.config

settings = yaml.load(open('settings.yml'))
logging.config.dictConfig(settings['logging'])
