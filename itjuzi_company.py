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
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from shared.common.common import Cm, dct_list_push
from shared.common.common import generate_logger,set_dct
from shared.db.entity import Project, Financing_phase, Company_member
from shared.conf.conf import db_connect_url, account, pltfm_r36k, task_server_url, db_connect_url_bisz_table_id_start, \
    chrome_options_using,pltfm_itjuzi
from shared.util.util import get_system_uuid



WRITE_DB = True
LINUX = True

display = None
engine = None
url_ls = ['https://www.itjuzi.com/company/10000', 'https://www.itjuzi.com/company/20000', 'https://www.itjuzi.com/company/30000','https://www.itjuzi.com/company/40000', 'https://www.itjuzi.com/company/50000', 'https://www.itjuzi.com/company/60000']
if LINUX:
    display = Display(visible=0, size=(1024, 768))
    display.start()
    url_get_worker_id = '{task_server_url}/assign_worker_id/{worker_system_uuid}'.format(worker_system_uuid=get_system_uuid(), task_server_url=task_server_url)
    resp_get_worker_id = json.load(urllib2.urlopen(url_get_worker_id))
    worker_id = resp_get_worker_id['worker_id']
    bisz_table_id_start = resp_get_worker_id['bisz_table_id_start']

    url_get_task = '{task_server_url}/allocate_task/{worker_id}/{investment_platform}/{entrance_url_cnt}'.format(worker_id=worker_id,
                                                                                              investment_platform=pltfm_itjuzi,
                                                                                              task_server_url=task_server_url,
                                                                                            entrance_url_cnt=50)
    resp_get_task = json.load(urllib2.urlopen(url_get_task))
    url_ls = [i['entrance_url'] for i in resp_get_task]

    engine = create_engine(db_connect_url_bisz_table_id_start.format(bisz_table_id_start=bisz_table_id_start))
else:
    engine = create_engine(db_connect_url)

DBSession = sessionmaker(bind=engine)
session = DBSession()
investment_platform = 'www.itjuzi.com'.encode('utf-8')
logging = generate_logger("itjuzi.log", "itjuzi")
detail_driver = None
detail_cm = None
def init_driver():
    global detail_driver
    global detail_cm
    detail_driver = webdriver.Chrome(chrome_options=chrome_options_using)  # chrome_options=chrome_options_using
    detail_driver.set_page_load_timeout(30)
    detail_cm = Cm(logging, detail_driver)


wrong_number = 0


def login():
    global detail_driver
    global detail_cm
    try:
        detail_driver.get('https://www.itjuzi.com/user/login')
        time.sleep(1)
        username = detail_driver.find_element_by_css_selector('[id=create_account_email]')
        password = detail_driver.find_element_by_css_selector('[id=create_account_password]')
        submit = detail_driver.find_element_by_css_selector('[id=login_btn]')
        if LINUX:
            url_get_platform_account = '{task_server_url}/get_platform_account/{investment_platform}'.format(investment_platform=pltfm_itjuzi, task_server_url=task_server_url)
            resp_get_platform_account = json.load(urllib2.urlopen(url_get_platform_account))
            usernameI = resp_get_platform_account['username']
            passwordI = resp_get_platform_account['pass']
            logging.info("platform,username[{username},password[{password}]]".format(password=passwordI, username=usernameI))
            username.send_keys(usernameI)
            password.send_keys(passwordI)
        else:
            username.send_keys('2437222483@qq.com')
            password.send_keys('881124')
        submit.click()
        time.sleep(1)
    except Exception as e:
        logging.exception('login fail')
        logging.exception(e)

def get_from_company_url(url):
    global detail_driver
    global detail_cm
    global wrong_number
    try:
        try:
            detail_driver.get(url);   time.sleep(1)
        except Exception as e:
            logging.exception(e)
            wrong_number += 1
            if wrong_number > 10:
                wrong_number = 0
                detail_driver.quit()
                init_driver()
                login()

        path = 'div.rowhead.feedback-btn-parent'; project_obj = detail_cm.find_elment_by_itjuzi(detail_driver.find_element_by_css_selector, path)

        path = 'div[2]/div[1]/span[1]/h1/span'; financing_phase = detail_cm.find_elment_by_itjuzi(project_obj.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
        if financing_phase=='':
            return
        path = "div[1] / img"; logo_url = detail_cm.find_elment_by_itjuzi(project_obj.find_element_by_xpath, path, attribt='src', rtValWhnErr='')
        path = "div[2] / div[1] / span[1] / h1"; name = detail_cm.find_elment_by_itjuzi(project_obj.find_element_by_xpath, path, using_txt=True, rtValWhnErr=''); name = name[0:name.find(financing_phase)-1]
        path = "div[2] / div[3] / span[1] / a[1]"; industry = detail_cm.find_elment_by_itjuzi(project_obj.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
        path = "div[2]/div[3]/span[2]/a[2]"; city = detail_cm.find_elment_by_itjuzi(project_obj.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
        financing_phase = financing_phase.strip('()')
        # path = "i[5]"; invest_amount = detail_cm.find_elment_by_itjuzi(project_obj.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
        # path = "i[6]/div"; investors = detail_cm.find_elment_by_itjuzi(project_obj.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
        path = "div[2]/div[4]/a[last()]";  site = detail_cm.find_elment_by_itjuzi(project_obj.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
        if site == '':
            path = 'div[2] / div[4] / span[1] / a[1]'
            site = detail_cm.find_elment_by_itjuzi(project_obj.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
            if site == '':
                path = 'div[2] / div[4] / span[1] / a[2]'
                site = detail_cm.find_elment_by_itjuzi(project_obj.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')

        path = "div.main"; detail_obj = detail_cm.find_elment_by_itjuzi(detail_driver.find_element_by_css_selector, path)

        introduction = ''
        path="/html/body/div[3]/div[5]/div[2]/div[1]/div[2]/div[2]/div[last()]";
        introduction = detail_cm.find_elment_by_itjuzi(detail_driver.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
        # path = "div.abstract:nth-child(2)"; introduction1 = detail_cm.find_elment_by_itjuzi(detail_obj.find_elements_by_css_selector, path,using_txt=True, rtValWhnErr='')
        # path = "div.introduction"; introduction2 = detail_cm.find_elment_by_itjuzi(detail_obj.find_elements_by_css_selector, path,using_txt=True, rtValWhnErr='')
        # introduction = introduction1 if introduction2 == '' else introduction2

        product_description = ''
        path = "ul.list-prod.limited-itemnum>li"; product_lst = detail_cm.find_elment_by_itjuzi(detail_obj.find_elements_by_css_selector, path)
        if len(product_lst)>0:
            product_obj = product_lst[0]
            path = "div[1]/p"; product_description = detail_cm.find_elment_by_itjuzi(product_obj.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')

        path = "div[1]/div[2]/div[3]/div/div[1]/h2"; company_name = detail_cm.find_elment_by_itjuzi(detail_obj.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
        company_name = company_name[company_name.find(u'：') + 1:]
        path = "div[1]/div[2]/div[3]/div/div[2]/h2"; start_date = detail_cm.find_elment_by_itjuzi(detail_obj.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
        start_date = start_date[start_date.find(u'：') + 1:]

        log_str = u'project（logo_url:%s、name:%s、introduction:%s、product_description:%s、industry:%s、city:%s, financing_phase:%s,company_name:%s, start_date:%s, site:%s）'
        logging.info(log_str % (logo_url, name, introduction, product_description, industry, city, financing_phase, company_name, start_date, site))

        if WRITE_DB:
            dbCursor = session.query(Project).filter(Project.name == name, Project.investment_platform == investment_platform)
            project = dbCursor.first()
            if dbCursor.count() == 0:
                project = Project(logo_url=logo_url,
                                  name=name,
                                  introduction=introduction,
                                  product_description=product_description,
                                  industry=industry,
                                  city=city,
                                  financing_phase=financing_phase,
                                  company_name=company_name,
                                  start_date=start_date,
                                  site=site,
                                  investment_platform=investment_platform)
                session.add(project)
                session.commit()
            else:
                dbCursor.update(
                    { Project.logo_url: logo_url, Project.name: name, Project.introduction: introduction,
                      Project.product_description: product_description,
                      Project.industry: industry, Project.city: city, Project.financing_phase: financing_phase,
                      Project.company_name: company_name,Project.start_date: start_date, Project.site: site, Project.investment_platform: investment_platform})
                session.commit()

        # 获投信息：时间、融资轮次、融资金额、投资方
        path = "table.list-round-v2>tbody>tr"; inves_list = detail_cm.find_elment_by_itjuzi(detail_obj.find_elements_by_css_selector, path)
        for inves in inves_list:
            try:
                path = "td[1]/span[1]"; date = detail_cm.find_elment_by_itjuzi(inves.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
                path = "td[2]/span/a"; phase = detail_cm.find_elment_by_itjuzi(inves.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
                path = "td[3]/span/a"; amount = detail_cm.find_elment_by_itjuzi(inves.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
                path = "td[4]"; investor = detail_cm.find_elment_by_itjuzi(inves.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
                if u'登录' in phase:
                    login()
                    return False
                logging.info(u'Financing_phase(phase：%s, amount:%s, investor:%s, date:%s)' % (phase,amount,investor,date))
                if WRITE_DB:
                    dbCursor = session.query(Financing_phase).filter(Financing_phase.phase==phase, Financing_phase.project_id == project.id)
                    if dbCursor.count() == 0:
                        fp = Financing_phase(phase=phase, amount=amount, investor=investor, date=date, project_id=project.id, investment_platform=investment_platform)
                        session.add(fp)
                        session.commit()
                    else:
                        dbCursor.update({Financing_phase.phase: phase, Financing_phase.amount: amount, Financing_phase.investor: investor,
                                         Financing_phase.date: date, Financing_phase.project_id: project.id, Financing_phase.investment_platform: investment_platform})
                        session.commit()
            except Exception as e:
                logging.exception(e)

        # 公司成员：姓名、职位、详细介绍
        path = "ul.list-prodcase.limited-itemnum>li"; company_list = detail_cm.find_elment_by_itjuzi(detail_obj.find_elements_by_css_selector, path)
        for company in company_list:
            try:
                path = "div/div[2]/h4/a[last()]/b/span[1]"
                comp_name = detail_cm.find_elment_by_itjuzi(company.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
                if comp_name == '':
                    break
                path = "div/div[2]/h4/a[last()]/b/span[2]"; position = detail_cm.find_elment_by_itjuzi(company.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
                path = "div/div[2]/p"; experience = detail_cm.find_elment_by_itjuzi(company.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
                logging.info(u'Company_member(name：%s, position:%s, experience:%s)' % (comp_name, position, experience))
                if WRITE_DB:
                    dbCursor = session.query(Company_member).filter(Company_member.name==comp_name, Financing_phase.project_id == project.id)
                    if dbCursor.count() == 0:
                        cmp = Company_member(name=comp_name, position=position, experience=experience, project_id = project.id, investment_platform=investment_platform)
                        session.add(cmp)
                        session.commit()
                    else:
                        dbCursor.update({Company_member.name: comp_name, Company_member.position: position, Company_member.experience: experience,
                                         Company_member.project_id: project.id, Company_member.investment_platform: investment_platform})
                        session.commit()
            except Exception as e:
                logging.exception(e)
    except Exception as e:
        logging.exception(e)
    return True

init_driver()
login()
# 一共84100多个

for url in url_ls:
    logging.info(url)
    get_from_company_url(url)


detail_driver.close()
detail_driver.quit()
session.close()
if LINUX:
    display.stop()

