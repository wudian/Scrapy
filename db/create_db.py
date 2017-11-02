#!/usr/bin/env pytho
# -*- coding:utf-8 -*-
import codecs
import urllib2

from flask import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from shared.common.common import generate_logger
from shared.conf.conf import task_server_url, db_connect_url4init
from shared.util.util import get_system_uuid
from jinja2 import Environment, FileSystemLoader
import random
import datetime
import time
import pymysql
import os
import os.path

db = pymysql.connect(host='localhost', port=3306, user='root', passwd='wudian', charset='utf8')

root_dir='C:\\Users\\za-wudian\\Desktop\\db'
merge_dir='D:\\py_prj\\Scrapy\\investment_platform_crawler\\merge_db'
env = Environment(loader=FileSystemLoader([root_dir, merge_dir]))

try:
    with db.cursor() as cursor:

        for parent, dirnames, filenames in os.walk(root_dir):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
            for filename in filenames:
                if '.defsql' in filename:
                    continue
                name, ext = os.path.splitext(filename)
                # sql_path = os.path.join(parent, filename)
                # db_name = name[0: name.index('_', 25)]
                db_name = name
                if 'mysqldatasql' in filename:
                    continue
                    # sql = "drop database %s" % db_name
                    # cursor.execute(sql)
                    # sql = "create database %s" % db_name
                    # cursor.execute(sql)
                    sql = "use %s" % db_name
                    cursor.execute(sql)
                    template_db_def = env.get_template(filename)
                    db_def_str = template_db_def.render()
                    with codecs.open("out_investment_platform_crawler-db-def.sql", "wb", "utf8") as fh:
                        fh.write(db_def_str)

                    cursor.execute(db_def_str)
                    db.commit()

                elif '.sql' in filename:
                    template_db_def = env.get_template('itjuzi_merge.sql')
                    db_def_str = template_db_def.render(from_db=db_name, to_db='investment_platform_db880700000')
                    with codecs.open("out_investment_platform_crawler-db-def.sql", "wb", "utf8") as fh:
                        fh.write(db_def_str)
                    # cursor.execute(sql)
                    cursor.execute(db_def_str)


        db.commit()

except Exception,e:
    print repr(e)
finally:
    cursor.close()