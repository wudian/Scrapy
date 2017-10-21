# -*- coding: utf-8 -*-
import codecs
import urllib2

from flask import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from shared.common.common import generate_logger
from shared.conf.conf import task_server_url, db_connect_url4init
from shared.util.util import get_system_uuid
from jinja2 import Environment, FileSystemLoader

logging = generate_logger("info.log", "itjuzi")
engine = create_engine(db_connect_url4init)
DBSession = sessionmaker(bind=engine)

session = DBSession()


url_get_worker_id = '{task_server_url}/assign_worker_id/{worker_system_uuid}'.format(worker_system_uuid=get_system_uuid(), task_server_url=task_server_url)
resp_get_worker_id=json.load(urllib2.urlopen(url_get_worker_id))

worker_id = resp_get_worker_id['worker_id']
bisz_table_id_start = resp_get_worker_id['bisz_table_id_start']

env = Environment(loader=FileSystemLoader(['/root/investment_platform_crawler/shared/db-def/template/jinja2'])  )
template_db_def = env.get_template('investment_platform_crawler-db-def.sql')
db_def_str = template_db_def.render(bisz_table_id_start=bisz_table_id_start)
with codecs.open("out_investment_platform_crawler-db-def.sql", "wb", "utf8") as fh:
    fh.write(db_def_str)

session.execute(db_def_str)

session.close()