import logging
from config import db_config
from psycopg2 import connect
from sys import exit


def connection():
	try:
		return connect(
			dbname=db_config['db_name'], user=db_config['user'], password=db_config['password'], host=db_config['host']
		)
	except:
		# Write logs...
		logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
		logging.error(f'Connection error to {db_config["host"]} -> {db_config["db_name"]}')
		exit(1)
