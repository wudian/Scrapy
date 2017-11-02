# encoding: UTF-8
import time
import traceback
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib2

from itertools import product
# from pyvirtualdisplay import Display

from flask import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
# import selenium.webdriver.common.action_chains.ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from shared.db.tree_entity import Project, Financing_phase, Company_member
from shared.common.common import generate_logger, Cm
from shared.conf.tree_conf import db_connect_url,  account, pltfm_tree
from shared.conf.conf import task_server_url, db_connect_url_bisz_table_id_start, chrome_options_using
from shared.util.util import get_system_uuid
import numpy as np

WRITE_DB = True
LINUX = False
updatemode = True

display = None
engine = None
url_ls = ['https://www.innotree.cn/company/1.html', 'https://www.innotree.cn/company/100.html', 'https://www.innotree.cn/company/1100.html']


# if LINUX:
#     display = Display(visible=0, size=(1024, 768))
#     display.start()
#     url_get_worker_id = '{task_server_url}/assign_worker_id/{worker_system_uuid}'.format(worker_system_uuid=get_system_uuid(), task_server_url=task_server_url)
#     resp_get_worker_id = json.load(urllib2.urlopen(url_get_worker_id))
#     worker_id = resp_get_worker_id['worker_id']
#     bisz_table_id_start = resp_get_worker_id['bisz_table_id_start']
#
#     url_get_task = '{task_server_url}/allocate_task/{worker_id}/{investment_platform}'.format(worker_id=worker_id,
#                                                                                               investment_platform=pltfm_tree,
#                                                                                               task_server_url=task_server_url)
#     resp_get_task = json.load(urllib2.urlopen(url_get_task))
#     url_ls = [i['entrance_url'] for i in resp_get_task]
#
#     engine = create_engine(db_connect_url_bisz_table_id_start.format(bisz_table_id_start=bisz_table_id_start))
# else:
#     engine = create_engine(db_connect_url)
engine = create_engine(db_connect_url)

# engine = create_engine(db_connect_url)
DBSession = sessionmaker(bind=engine)
session = DBSession()



investment_platform = 'www.innotree.cn'.encode('utf-8')
logging = generate_logger("innotree-info.log", "innotree")

# 设置浏览器
# driver = webdriver.Chrome(chrome_options=chrome_options_using)
detail_driver = webdriver.Chrome(chrome_options=chrome_options_using)
detail_driver.maximize_window()
# cm = Cm(logging, driver)
detail_cm = Cm(logging, detail_driver)

url_get_platform_account = '{task_server_url}/get_platform_account/{investment_platform}'.format(investment_platform=pltfm_tree ,task_server_url=task_server_url)

# def login():
# driver.get('https://www.innotree.cn/#login')
# time.sleep(0.5)
detail_driver.get('https://www.innotree.cn/#login')
time.sleep(1) # Let the user actually see something!

username = detail_driver.find_element_by_class_name('sign_in_input01')
password = detail_driver.find_element_by_class_name('sign_in_input02')
submit = detail_driver.find_element(By.XPATH,'//*[@id="login_form_y"]/div[4]/input')

if LINUX:
    url_get_platform_account = '{task_server_url}/get_platform_account/{investment_platform}'.format(
        investment_platform=pltfm_tree, task_server_url=task_server_url)
    resp_get_platform_account = json.load(urllib2.urlopen(url_get_platform_account))
    usernameI = resp_get_platform_account['username']
    passwordI = resp_get_platform_account['pass']
    logging.info("platform,username[{username},password[{password}]]".format(password=passwordI, username=usernameI))
    username.send_keys(usernameI)
    password.send_keys(passwordI)
else:
    username.send_keys('18616858682')
    password.send_keys('123456')

submit.click()
time.sleep(1)

# login()


cid_list = np.arange(5000, 10000)      # 项目编号
url_ls = []
url_ls_checked = []

for cid in cid_list:
    # cid = proj.get_attribute('data-cid')
    url_tmp = 'https://www.innotree.cn/company/' + str(cid) + '.html'   # 生成项目详情页网址
    url_ls.append(url_tmp)

# url_ls = ['https://www.innotree.cn/company/298.html']
for url in url_ls:
    logging.info(url)
    try:
        detail_driver.get(url)    # 打开详情页
        # detail_driver.implicitly_wait(10)
        time.sleep(5)
    except Exception as e:
        logging.exception(e)
        logging.error(u'无法打开详情页！')
        logging.error(e)
        continue

    # 项目名称
    # path = 'div/div[1]/table/tbody/tr/td[2]/div/div[2]/h3'; name = cm.find_elment_by(proj.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
    path = '/html/body/div[2]/div[2]/div[1]/table/tbody/tr/td[2]/h3'; name = detail_cm.find_elment_by(detail_driver.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
    if name == '':
        logging.info(u'无法打开详情页！')
        continue
    logging.info(name)
    url_ls_checked.append(url)  # 将有项目的网址保存下来备用
    dbCursor = session.query(Project).filter(Project.name == name, Project.investment_platform == investment_platform)

    if dbCursor.count() > 0 and not updatemode:
        logging.info(u'跳过已保存项目')
        continue

    project = dbCursor.first()

    logging.info(u'有效网址已保存,开始爬数据')
    # 开始爬字段
    try:
        # 当前融资轮次、公司全称、logo_url
        path = '/html/body/div[2]/div[2]/div[1]/table/tbody/tr/td[2]/p/span'; f_phase = detail_cm.find_elment_by(detail_driver.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
        # 公司全称
        path = '/html/body/div[2]/div[2]/div[1]/table/tbody/tr/td[2]/p'; company_name = detail_cm.find_elment_by(detail_driver.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
        company_name = company_name[0:company_name.find(f_phase) - 1] # 查到的公司全称去掉融资轮次字符串
        path = '/html/body/div[2]/div[2]/div[1]/table/tbody/tr/td[1]/div/img'; logo_url = detail_cm.find_elment_by(detail_driver.find_element_by_xpath, path, attribt='src', rtValWhnErr='')

        # 公司简介、网址、行业
        path = '/html/body/div[2]/div[4]'; introduction = detail_cm.find_elment_by(detail_driver.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
        path = '/html/body/div[2]/div[2]/div[2]/table/tbody/tr/td[1]/div[2]/div[1]/a'; site = detail_cm.find_elment_by(detail_driver.find_element_by_xpath, path, attribt='href', rtValWhnErr='')
        path = '/html/body/div[2]/div[2]/div[2]/table/tbody/tr/td[1]/div[1]/div/a[2]'; industry = detail_cm.find_elment_by(detail_driver.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')

        path = 'btn_finance_more_open'; btn_finance_more = detail_cm.find_elment_by(detail_driver.find_element_by_id, path)
        path = 'business_open'; btn_business_more = detail_cm.find_elment_by(detail_driver.find_element_by_id, path)
        if btn_finance_more is not None:
            btn_finance_more.click()
            time.sleep(1)
            logging.info(u'融资情况查看更多')
        else:
            logging.warning(u'===没有融资情况查看更多按钮')
        if btn_business_more is not None:
            btn_business_more.click()
            time.sleep(1)
            logging.info(u'工商注册情况查看更多')
        else:
            logging.warning(u'===没有工商注册查看更多按钮')
        # try:
        #     # btn2 = detail_driver.find_element(By.XPATH, '//*[@id="btn_finance_more_open"]')
        #     btn2 = detail_driver.find_element(By.ID, 'btn_finance_more_open')
        #     btn2.click()  # 点击融资情况查看更多
        #     detail_driver.implicitly_wait(10)
        #     time.sleep(1)
        #     logging.info(u'融资情况查看更多')
        #     # fphase_more = True
        # except Exception as e:
        #     logging.exception(e)
        #     # fphase_more = False
        #     logging.warning(u'融资情况没有查看更多按钮')
        # try:
        #     btn2 = detail_driver.find_element(By.ID, 'business_open')
        #     btn2.click()  # 点击工商注册查看更多
        #     detail_driver.implicitly_wait(10)
        #     time.sleep(1)
        #     logging.info(u'工商注册情况查看更多')
        #     # info_more = True
        # except Exception as e:
        #     logging.exception(e)
        #     # info_more = False
        #     logging.warning(u'工商注册没有查看更多按钮')

        # 融资情况模块（有些项目没有该模块，会导致xpath改变，用class name定位）
        path = '.details_1221_d03'
        fnc_info = detail_cm.find_elment_by(detail_driver.find_elements_by_css_selector, path)  # 融资情况模块

        # 已融资额度(有些项目有，有些没有）
        if len(fnc_info) > 0:
            path = 'div[2]/span'; raised_fund = detail_cm.find_elment_by(fnc_info[0].find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
        else:
            raised_fund = ''

        # 工商注册模块（有些项目没有该模块，会导致xpath改变，用class name定位）
        path = '.details_1221_d04'
        reg_info = detail_cm.find_elment_by(detail_driver.find_elements_by_css_selector, path)  # 工商注册模块

        # 注册时间、公司地址
        if len(reg_info) > 0:
            path = 'div[2]/table/tbody/tr/td[3]/h3'; start_date = detail_cm.find_elment_by(reg_info[0].find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
            path = 'div[3]/table/tbody/tr/td[2]/div/div[9]/table/tbody/tr/td[2]/span'; address = detail_cm.find_elment_by(reg_info[0].find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
        else:
            start_date = ''
            address = ''

        logging.info(u'------基本信息-------')
        logging.info('url: %s' % url)
        logging.info('name: %s' % name)
        logging.info('company_name: %s' % company_name)
        logging.info('logo_url: %s' % logo_url)
        logging.info('introduction: %s' % introduction)
        logging.info('industry: %s' % industry)
        logging.info('site: %s' % site)
        logging.info('f_phase: %s' % f_phase)
        logging.info('raised_fund: %s' % raised_fund)
        logging.info('start_date: %s' % start_date)
        logging.info('address: %s' % address)

    except Exception as e:
        logging.exception(e)
        logging.error(u'出现错误')
        logging.error(e)

    # 将项目各项信息存入数据库Project表
    try:
        # dbCursor = session.query(Project).filter(Project.name == name, Project.investment_platform == investment_platform)
        # project = dbCursor.first()
        if dbCursor.count() == 0 and WRITE_DB:
            logging.info(u'保存新数据...')
            project = Project(logo_url=logo_url, name=name, introduction=introduction, industry=industry, financing_phase=f_phase, raised_fund=raised_fund, company_name=company_name, start_date=start_date, investment_platform=investment_platform, site=site, address=address)
            session.add(project)
            session.commit()
        elif updatemode and WRITE_DB:
            logging.info(u'更新数据')
            dbCursor.update({'logo_url':logo_url, 'name':name, 'introduction':introduction, 'industry':industry, 'financing_phase':f_phase, 'raised_fund':raised_fund, 'company_name':company_name, 'start_date':start_date, 'investment_platform':investment_platform, 'site':site, 'address':address})
            session.commit()
        # else:
        #     logging.info(u'跳过已保存数据')
    except Exception as e:
        logging.exception(e)
        logging.error(u'出现错误')
        logging.error(e)

    # 当项目基本信息顺利查完并保存到数据库，继续查融资情况和创始团队信息
    dbCursor = session.query(Project).filter(Project.name == name, Project.investment_platform == investment_platform)
    project = dbCursor.first()
    if dbCursor.count() > 0:
        # 融资情况
        try:
            path = '//*[@id="finance_list"]/table/tbody/tr'
            finfo_list = detail_cm.find_elment_by(detail_driver.find_elements_by_xpath, path)
            # finfo_list = detail_driver.find_elements(By.XPATH, '//*[@id="finance_list"]/table/tbody/tr')
            for finfo in finfo_list:
                path = 'td[1]/p'; phase = detail_cm.find_elment_by(finfo.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
                path = 'td[2]/p'; amount = detail_cm.find_elment_by(finfo.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
                path = 'td[3]'; investor = detail_cm.find_elment_by(finfo.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
                path = 'td[4]'; inves_date = detail_cm.find_elment_by(finfo.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
                logging.info(u'------融资情况-------')
                logging.info('phase: %s' % phase)
                logging.info('amount: %s' % amount)
                logging.info('investor: %s' % investor)
                logging.info('inves_date: %s' % inves_date)
                # 查询数据库是否已经存在该融资轮次信息
                dbCursor2 = session.query(Financing_phase).filter(Financing_phase.phase == phase, Financing_phase.project_id == project.id)
                if dbCursor2.count() == 0 and WRITE_DB:
                    data_fp = Financing_phase(phase=phase, amount=amount, investor=investor, date=inves_date,
                                         project_id=project.id, investment_platform=investment_platform)
                    session.add(data_fp)
                    session.commit()
                    logging.info(u'新增融资经历')
                elif updatemode and WRITE_DB:
                    logging.info(u'更新已保存数据')
                    dbCursor2.update({'phase':phase,'amount':amount, 'investor':investor,'date':inves_date,'project_id':project.id, 'investment_platform':investment_platform})
                    session.commit()
                else:
                    logging.info(u'跳过已保存数据')

        except Exception as e:
            logging.exception(e)
            logging.error(u'出现错误')
            logging.error(e)
            logging.warning(u'该项目没有融资情况信息')

        try:
            # ActionChains(detail_driver) . key_down( Keys.PAGE_DOWN).perform(); time.sleep(0.5)
            # ActionChains(detail_driver) . key_down( Keys.PAGE_DOWN).perform(); time.sleep(0.5)
            # ActionChains(detail_driver) . key_down( Keys.PAGE_DOWN).perform(); time.sleep(0.5)
            # member_list = driver2.find_elements(By.XPATH, '/html/body/div[2]/div[13]/div/div')
            path = '.founding_team_list'
            member_list = detail_cm.find_elment_by(detail_driver.find_elements_by_css_selector, path)
            # member_list = driver2.find_elements(By.CSS_SELECTOR, '.founding_team_list')
            for member in member_list:
                path = 'div[2]/h5'; member_name = detail_cm.find_elment_by(member.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
                path = 'div[2]/span'; member_pos = detail_cm.find_elment_by(member.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
                path = 'div[2]/div/p'; member_exp = detail_cm.find_elment_by(member.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
                path = 'div[2]'; member_info = detail_cm.find_elment_by(member.find_element_by_xpath, path)
                if member_info != None:
                    # ActionChains(detail_driver).move_to_element_with_offset(member_exp2, 10, 10).perform()
                    ActionChains(detail_driver).move_to_element(member_info).click().perform(); time.sleep(2)

                    member_info = member_info.text
                    # logging.info('ertyuiop[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[%s' % member_info)
                    member_info = member_info.split('\n')
                    # logging.info('ertyuiop[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[%s' % member_info)
                    member_info1 = member_info[0].split(' ')
                    if len(member_info1) == 2 and member_pos == '':
                        member_pos = member_info1[1]
                    if len(member_info) == 3:
                        member_exp = member_info[2]
                    # logging.info('ertyuiop[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[%s' % member_exp)

                # time.sleep(3)
                # detail_driver.get_screenshot_as_file('move_mouse.png')
                # path = 'div[2]/div/div'; member_exp2 = detail_cm.find_elment_by(member.find_element_by_xpath, path)
                # if member_exp == '':
                #     path = 'div[2]/div/p'; member_exp = detail_cm.find_elment_by(member.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
                logging.info(u'------创始团队-------')
                logging.info('name: %s' % member_name)
                logging.info('position: %s' % member_pos)
                logging.info('experience: %s' % member_exp)

                dbCursor3 = session.query(Company_member).filter(Company_member.name == member_name, Company_member.project_id == project.id)
                if dbCursor3.count() == 0 and WRITE_DB:
                    data_cmember = Company_member(name=member_name, position=member_pos, experience=member_exp,
                                        project_id=project.id, investment_platform=investment_platform)
                    session.add(data_cmember)
                    session.commit()
                    logging.info(u'新增创始团队')
                elif updatemode and WRITE_DB:
                    logging.info(u'更新已保存数据')
                    dbCursor3.update({'name': member_name, 'position': member_pos, 'experience': member_exp, 'project_id': project.id, 'investment_platform': investment_platform})
                    session.commit()
                else:
                    logging.info(u'跳过已保存数据')

        except Exception as e:
            logging.exception(e)
            logging.error(u'出现错误')
            logging.error(e)
            logging.warning(u'该项目没有创始团队信息')
    logging.info(u'-----------完成----------')

session.close()
detail_driver.quit()

logging.info(u'-----------完成----------')

# 将有效网址保存到json
# 先读取已有url
urlsaved_filename = 'innotree_url.json'
fileObj = open(urlsaved_filename, 'r')
d = json.load(fileObj)
url_ls_checked_old = d['url_ls_checked']
fileObj.close()

url_ls_checked_new = list(set(url_ls_checked_old+url_ls_checked))
d = {}
d['url_ls_checked'] = url_ls_checked_new
jsObj = json.dumps(d)
fileObject = open(urlsaved_filename,'w')
fileObject.write(jsObj)
fileObject.close()