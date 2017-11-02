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
    chrome_options_using
from shared.util.util import get_system_uuid

# display = Display(visible=0, size=(1024, 768))
# display.start()


investment_platform = 'www.itjuzi.com'.encode('utf-8')
logging = generate_logger("it_orange.log", "it_orange")
engine = create_engine(db_connect_url)
DBSession = sessionmaker(bind=engine)

session = DBSession()
# chrome_options=chrome_options_using
driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
detail_driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
cm = Cm(logging, driver)
detail_cm = Cm(logging, detail_driver)

url_get_platform_account = '{task_server_url}/get_platform_account/{investment_platform}'.format(investment_platform=pltfm_r36k ,task_server_url=task_server_url)


def login():
    driver.get('https://www.itjuzi.com/user/login')
    detail_driver.get('https://www.itjuzi.com/user/login')
    time.sleep(1) # Let the user actually see something!

    resp_get_platform_account = json.load(urllib2.urlopen(url_get_platform_account))
    usernameI = resp_get_platform_account['username']
    passwordI = resp_get_platform_account['pass']
    logging.info("platform,username[{username},password[{password}]]".format(password=passwordI, username=usernameI))
    username = detail_driver.find_element_by_css_selector('[id=create_account_email]')
    password = detail_driver.find_element_by_css_selector('[id=create_account_password]')
    submit = detail_driver.find_element_by_css_selector('[id=login_btn]')
    username.send_keys(usernameI)
    password.send_keys(passwordI)
    submit.click()
    time.sleep(1)

    username = driver.find_element_by_css_selector('[id=create_account_email]')
    password = driver.find_element_by_css_selector('[id=create_account_password]')
    submit = driver.find_element_by_css_selector('[id=login_btn]')
    username.send_keys(usernameI)
    password.send_keys(passwordI)
    submit.click()
    time.sleep(1)

login()

for pageno in range(20, 21000):
    logging.info('pageno:%d' % pageno)
    driver.get('https://www.itjuzi.com/investevents?page=%d' % pageno)
    ng_scope_ls = cm.find_elment_by(driver.find_elements_by_css_selector, "ul.list-main-eventset>li")
    for i in range(1, len(ng_scope_ls)):
        try:
            ng_scope = ng_scope_ls[i]
            # 项目列表（时间、公司logo、公司、轮次、融资额、投资方）
            # path = "i/span"; time = cm.find_elment_by(ng_scope.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
            logo_url = cm.find_elment_by(ng_scope.find_element_by_xpath, "i[2]/a/span/img", attribt='src', rtValWhnErr='')
            path = "i[3]/p/a/span"; name = cm.find_elment_by(ng_scope.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
            path = "i[3]/p[2]/span/a"; industry = cm.find_elment_by(ng_scope.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
            path = "i[3]/p[2]/span[2]/a"; city = cm.find_elment_by(ng_scope.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
            path = "i[4]/a/span"; financing_phase = cm.find_elment_by(ng_scope.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
            path = "i[5]"; invest_amount = cm.find_elment_by(ng_scope.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
            path = "i[6]/div"; investors = cm.find_elment_by(ng_scope.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
            # 项目详情页：
            path = "i[3]/p/a"; detail_url = cm.find_elment_by(ng_scope.find_element_by_xpath, path, attribt='href', rtValWhnErr='')
            detail_driver.get(detail_url);       detail_driver.implicitly_wait(10)
            # 基本信息：公司简介、公司全称、成立时间、公司规模
            path = "div.main"; details = detail_cm.find_elment_by(detail_driver.find_elements_by_css_selector, path)
            if type(details)==list:
                details = details[0]

            path = "div[1]/div[2]/div[2]/div";  introduction = detail_cm.find_elment_by(details.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
            if introduction == '':
                path = "div[1]/div[2]/div[2]/div[2]"
                introduction = detail_cm.find_elment_by(details.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
            path = "div[5]/div[2]/ul/li/div[1]/h4/b/a"; site = detail_cm.find_elment_by(details.find_element_by_xpath, path, attribt='href', rtValWhnErr='')
            if site == '':
                path = "div[6]/div[2]/ul/li/div[1]/h4/b/a"
                site = detail_cm.find_elment_by(details.find_element_by_xpath, path, attribt='href', rtValWhnErr='')
            path = 'div[5]/div[2]/ul/li/div[1]/p'; product_description = detail_cm.find_elment_by(details.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
            if product_description == '':
                path = 'div[6]/div[2]/ul/li/div[1]/p'
                product_description = detail_cm.find_elment_by(details.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')

            path = "div[1]/div[2]/div[3]/div/div[1]/h2"; company_name = detail_cm.find_elment_by(details.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
            company_name = company_name[company_name.find(u'：') + 1:]
            path = "div[1]/div[2]/div[3]/div/div[2]/h2"; start_date = detail_cm.find_elment_by(details.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
            start_date = start_date[start_date.find(u'：') + 1:]
            # path = "div[1]/div[2]/div[3]/div/div[2]/h2[2]"; scale = error2null(detail_driver, details.find_element, By.XPATH, path).text # 规模

            log_str = u'project（logo_url:%s、name:%s、introduction:%s、product_description:%s、industry:%s、city:%s, financing_phase:%s,company_name:%s, start_date:%s, site:%s）'
            logging.info(log_str % (logo_url, name, introduction, product_description, industry, city, financing_phase, company_name, start_date, site))
            # 指向某一项目名称的数据条，判断是否已经存在
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
            path = "table.list-round-v2>tbody>tr"; inves_list = detail_cm.find_elment_by(details.find_elements_by_css_selector, path)
            for inves in inves_list:
                try:
                    path = "td[1]/span[1]"; date = detail_cm.find_elment_by(inves.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
                    path = "td[2]/span/a"; phase = detail_cm.find_elment_by(inves.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
                    path = "td[3]/span/a"; amount = detail_cm.find_elment_by(inves.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
                    path = "td[4]"; investor = detail_cm.find_elment_by(inves.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
                    if u'登录' in phase:
                        login()
                        detail_driver.get(detail_url)
                        driver.get('https://www.itjuzi.com/investevents?page=%d' % pageno)
                        detail_driver.implicitly_wait(10)
                        continue
                    logging.info(u'Financing_phase(phase：%s, amount:%s, investor:%s, date:%s)' % (phase,amount,investor,date))
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
                    print e
                    traceback.print_exc()

            # 公司成员：姓名、职位、详细介绍
            path = "ul.list-prodcase.limited-itemnum>li"; company_list = detail_cm.find_elment_by(details.find_elements_by_css_selector, path)
            for company in company_list:
                try:
                    path = "div/div[2]/h4/a[last()]/b/span[1]"
                    comp_name = detail_cm.find_elment_by(company.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
                    if comp_name == '':
                        break
                    path = "div/div[2]/h4/a[last()]/b/span[2]"; position = detail_cm.find_elment_by(company.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
                    path = "div/div[2]/p"; experience = detail_cm.find_elment_by(company.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
                    logging.info(u'Company_member(name：%s, position:%s, experience:%s)' % (comp_name, position, experience))
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
                    print e
                    traceback.print_exc()
        except Exception as e:
            print e
            traceback.print_exc()
            # print inves_man

# driver.quit()
