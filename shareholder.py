# -*- coding: utf-8 -*-
import time
import traceback
import sys
import urllib2
from itertools import product

from pyvirtualdisplay import Display


from flask import json
from selenium import webdriver
# from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import  Keys
from selenium.webdriver.common.keys import Keys
from sqlalchemy import create_engine, not_
from sqlalchemy.orm import sessionmaker

import re
sys.path.append(r'C:\Users\za-wudian\Desktop\scrapy')
from shared.common.common import Cm, dct_list_push
from shared.common.common import generate_logger,set_dct
from shared.db.entity import Project, Financing_phase, Company_member, Shareholder, Company
from shared.conf.itjuzi_conf import db_connect_url, account, pltfm_r36k, task_server_url, db_connect_url_bisz_table_id_start, \
    chrome_options_using,pltfm_itjuzi
from shared.util.util import get_system_uuid



WRITE_DB = True
LINUX = False

display = None
engine = None
driver = None
detail_cm = None
wrong_number = 0

engine = create_engine(db_connect_url)

DBSession = sessionmaker(bind=engine)
session = DBSession()
investment_platform = 'www.itjuzi.com'.encode('utf-8')
logging = generate_logger("tianyancha.log", "tianyancha")

left = re.compile(u'（')
right = re.compile(u'）')

def login():
    try:
        global driver
        global detail_cm
        if LINUX:
            driver = webdriver.Chrome(chrome_options=chrome_options_using)  # chrome_options=chrome_options_using
        else:
            driver = webdriver.Chrome()
        driver.set_page_load_timeout(60)
        detail_cm = Cm(logging, driver)



        driver.get('https://www.tianyancha.com/login')
        time.sleep(1)

        login_obj = detail_cm.find_elment_by_itjuzi(driver.find_elements_by_css_selector, 'div.module.module1.module2.loginmodule.collapse.in>div')
        username = detail_cm.find_elment_by_itjuzi(login_obj[1].find_element_by_xpath, 'div[2] / input')
        password = detail_cm.find_elment_by_itjuzi(login_obj[1].find_element_by_xpath, 'div[3] / input')
        submit = detail_cm.find_elment_by_itjuzi(login_obj[1].find_element_by_xpath, 'div[5]')
        username.send_keys('18621528717')
        password.send_keys('bijia881124')
        submit.click()
        time.sleep(10)
    except Exception as e:
        logging.exception('login fail')
        logging.exception(e)
        # if 'server detect i am machine' == e.message:
            # 'list' object has no attribute 'find_element_by_xpath'
            # ip被封了 重启vpn
            # sys.exit()

def insert_db_dirty(project_id):
    global session
    try:
        if WRITE_DB:
            item = Shareholder(project_id=project_id)
            session.add(item)
            session.commit()
    except Exception as e:
        session.close()
        session = DBSession()
        logging.exception(e)


def get_from_shareholder(url, project_id, company_name):
    global driver
    global detail_cm
    global session
    time.sleep(30)
    driver.get(url)
    time.sleep(30)

    path = '_container_holder'; obj = detail_cm.find_elment_by_itjuzi(driver.find_element_by_id, path)
    if obj==None:
        logging.error(u'网页打不开')
        insert_db_dirty(project_id)
        return
    path = 'div/table/tbody/tr'; holders = detail_cm.find_elment_by_itjuzi(obj.find_elements_by_xpath, path)
    for holder in holders:
        path = 'td[1]/a'; name = detail_cm.find_elment_by_itjuzi(holder.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
        path = 'td[2]/div/div/span'; rate = detail_cm.find_elment_by_itjuzi(holder.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
        path = 'td[3]/div/span[1]'; amount = detail_cm.find_elment_by_itjuzi(holder.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
        path = 'td[3]/div/span[2]'; time_ = detail_cm.find_elment_by_itjuzi(holder.find_element_by_xpath, path, using_txt=True, rtValWhnErr=''); time_ = time_[time_.find(u'：')+1:]
        log_str = u'shareholder（name:%s,rate:%s, amount:%s, project_id:%s, time:%s, company_name:%s）' % (name, rate, amount, project_id, time_, company_name)
        logging.info(log_str)

        try:
            if WRITE_DB:
                dbCursor = session.query(Shareholder).filter(Shareholder.name == name, Shareholder.project_id == project_id)
                if dbCursor.count() == 0:
                    item = Shareholder(name=name, rate=rate, amount=amount, project_id=project_id, time=time_, project_name=company_name, investment_platform=investment_platform)
                    session.add(item)
                    session.commit()
                else:
                    dbCursor.update({Shareholder.name: name, Shareholder.rate: rate,
                                     Shareholder.amount: amount, Shareholder.project_id: project_id, Shareholder.time:time_,
                                     Shareholder.project_name:company_name, Shareholder.investment_platform:investment_platform})
                    session.commit()
        except Exception as e:
            session.close()
            session = DBSession()
            logging.exception(e)


def get_from_company_list():
    global driver
    global detail_cm
    global session
    try:
        while True:
            old_project_ids = session.query(Shareholder.project_id).group_by(Shareholder.project_id).all()
            old_ids = []
            for i in  old_project_ids:
                old_ids.append(i[0])
            new_list = session.query(Project.company_name, Project.id).filter(Project.investment_platform == investment_platform, not_(Project.id.in_(old_ids))).limit(5).all()
            if len(new_list) == 0:
                break
            for company_name in new_list:
                print company_name[0].encode("UTF-8")
                path = 'https://www.tianyancha.com/search?key=%s&checkFrom=searchBox' % company_name[0]
                driver.get(path)
                path = "div.b-c-white.search_result_container>div"
                company_list = detail_cm.find_elment_by_itjuzi(driver.find_elements_by_css_selector, path)

                is_exist = False
                for company in company_list:
                    path = "div[2] / div[1] / a / span"
                    name = detail_cm.find_elment_by_itjuzi(company.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
                    name = left.sub('(', name)
                    name = right.sub(')', name)
                    if name == company_name[0]:
                        path = "div[2]/div[1]/a"
                        url = detail_cm.find_elment_by_itjuzi(company.find_element_by_xpath, path, attribt='href', rtValWhnErr='')
                        try:
                            get_from_shareholder(url, company_name[1], company_name[0])
                        except Exception as e:
                            logging.exception(e)
                            driver.quit()
                            login()
                        is_exist = True
                        break

                if not is_exist:
                    logging.error("no company: %s" % company_name[0])
                    insert_db_dirty(company_name[1])

    except Exception as e:
        logging.exception(e)


def get_from_company_list2():
    global driver
    global detail_cm
    global session
    try:
        while True:
            id_list = []
            file = open(r'C:\Users\za-wudian\Desktop\scrapy\id.txt')
            while 1:
                line = file.readline()
                if not line:
                    break
                id_list.append(int(line))

            new_list = session.query(Project.company_name, Project.id).filter(Project.id.in_(id_list)).limit(10).all()
            
            for company_name in new_list:
                print company_name[0].encode("UTF-8")
                path = 'https://www.tianyancha.com/search?key=%s&checkFrom=searchBox' % company_name[0]
                driver.get(path)
                path = "div.b-c-white.search_result_container>div"
                company_list = detail_cm.find_elment_by_itjuzi(driver.find_elements_by_css_selector, path)

                is_exist = False
                for company in company_list:
                    path = "div[2] / div[1] / a / span"
                    name = detail_cm.find_elment_by_itjuzi(company.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
                    name = left.sub('(', name)
                    name = right.sub(')', name)
                    if name == company_name[0]:
                        path = "div[2]/div[1]/a"
                        url = detail_cm.find_elment_by_itjuzi(company.find_element_by_xpath, path, attribt='href', rtValWhnErr='')
                        try:
                            get_from_shareholder(url, company_name[1], company_name[0])
                        except Exception as e:
                            logging.exception(e)
                            driver.quit()
                            login()
                        is_exist = True
                        break

                if not is_exist:
                    logging.error("no company: %s" % company_name[0])
                    insert_db_dirty(company_name[1])

    except Exception as e:
        logging.exception(e)

def get_from_company_list3():
    global driver
    global detail_cm
    global session
    try:
        while True:
            old_project_ids = session.query(Shareholder.company_id).group_by(Shareholder.company_id).all()
            old_ids = []
            for i in  old_project_ids:
                old_ids.append(i[0])
            new_list = session.query(Company.company_name, Company.id).filter(not_(Company.id.in_(old_ids))).limit(10).all()
            if len(new_list) == 0:
                break
            for company_name in new_list:
                if not company_name[0]:
                    continue
                print company_name[0].encode("UTF-8")
                path = 'https://www.tianyancha.com/search?key=%s&checkFrom=searchBox' % company_name[0]
                driver.get(path)
                path = "div.b-c-white.search_result_container>div"
                company_list = detail_cm.find_elment_by_itjuzi(driver.find_elements_by_css_selector, path)

                is_exist = False
                for company in company_list:
                    path = "div[2] / div[1] / a / span"
                    name = detail_cm.find_elment_by_itjuzi(company.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
                    name = left.sub('(', name)
                    name = right.sub(')', name)
                    if name == company_name[0]:
                        path = "div[2]/div[1]/a"
                        url = detail_cm.find_elment_by_itjuzi(company.find_element_by_xpath, path, attribt='href', rtValWhnErr='')
                        try:
                            get_from_shareholder(url, company_name[1], company_name[0])
                        except Exception as e:
                            logging.exception(e)
                            driver.quit()
                            login()
                        is_exist = True
                        break

                if not is_exist:
                    logging.error("no company: %s" % company_name[0])
                    insert_db_dirty(company_name[1])

    except Exception as e:
        logging.exception(e)

if __name__ == '__main__':
    login()
    get_from_company_list3()



    driver.close()
    driver.quit()
    session.close()
    if LINUX:
        display.stop()

