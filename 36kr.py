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

display = Display(visible=0, size=(1024, 768))
display.start()


logging = generate_logger("info.log", "36kr")
driver = webdriver.Chrome(chrome_options=chrome_options_using)
cm = Cm(logging, driver)

# start_page = cm.s2int(sys.argv[1],1)
start_page = 1
driver.get('https://passport.36kr.com/pages/#/login')
# time.sleep(1) # Let the user actually see something!
time.sleep(1)
username = driver.find_element_by_css_selector('[id=kr-shield-username]')
password = driver.find_element_by_css_selector('[id=kr-shield-password]')
submit = driver.find_element_by_css_selector('[id=kr-shield-submit]')

url_get_platform_account = '{task_server_url}/get_platform_account/{investment_platform}'.format(investment_platform=pltfm_r36k ,task_server_url=task_server_url)
resp_get_platform_account=json.load(urllib2.urlopen(url_get_platform_account))
usernameI = resp_get_platform_account['username']
passwordI = resp_get_platform_account['pass']
logging.info("platform,username[{username},password[{password}]]".format(password=passwordI,username=usernameI))

username.send_keys(usernameI)
password.send_keys(passwordI)
submit.click()
time.sleep(1.5)
# jQuery.each($(".col-item.ng-scope"),function(){
#     console.info($(this).attr('data-stat-click'));
# })
url_get_worker_id = '{task_server_url}/assign_worker_id/{worker_system_uuid}'.format(worker_system_uuid=get_system_uuid(), task_server_url=task_server_url)
resp_get_worker_id=json.load(urllib2.urlopen(url_get_worker_id))
worker_id = resp_get_worker_id['worker_id']
bisz_table_id_start = resp_get_worker_id['bisz_table_id_start']

url_get_task = '{task_server_url}/allocate_task/{worker_id}/{investment_platform}'.format( worker_id = worker_id, investment_platform='rong.36kr.com',task_server_url=task_server_url )
resp_get_task=json.load(urllib2.urlopen(url_get_task))
url_ls = [ i['entrance_url']  for i in resp_get_task]

engine = create_engine(db_connect_url_bisz_table_id_start.format(bisz_table_id_start=bisz_table_id_start))
DBSession = sessionmaker(bind=engine)

session = DBSession()

page_size = 20

for url in url_ls:
    driver.get(url); time.sleep(2)
    path = "div.result-tip span b"; total_cnt_this_condition = cm.find_elment_by(driver.find_element_by_css_selector, path, using_txt=True, rtValWhnErr='0')
    logging.info("condition url:[%s],total_cnt_this_condition:%s"%(url,total_cnt_this_condition))
    end_page = (int(total_cnt_this_condition) + 20) / page_size
    for pagei in range(start_page,end_page+1,1):
        try:
            urlp = '{url}&p={pagei}'.format(url=url, pagei=pagei)
            logging.info("pageI url:%s"%urlp)
            driver.get(urlp); time.sleep(1.5)
            path = "tr.ng-scope"; ng_scope_ls = cm.find_elment_by( driver.find_elements_by_css_selector, path)
            assert len(ng_scope_ls) > 0
            project_name = None
            path = "td[1]/div/div[1]"; project_name_last_text = cm.find_elment_by( ng_scope_ls[len(ng_scope_ls)-1].find_element_by_xpath, path).text
            logging.info(u'last project name at this page. {project_name_last_text}'.format(project_name_last_text = project_name_last_text))
            for ng_scope in ng_scope_ls:
                try:
                    path = "td[1]/a"; project_logoi = cm.find_elment_by( ng_scope.find_element_by_xpath, path)
                    path = "td[1]/div/div[1]"; project_namei = cm.find_elment_by( ng_scope.find_element_by_xpath, path)#F5未来商店
                    path = "td[1]/div/div[2]"; project_intro_no_binding = cm.find_elment_by( ng_scope.find_element_by_xpath, path)#24小时无人便利店
                    path = "td[1]/div/div[3]"; project_tagi = cm.find_elment_by( ng_scope.find_element_by_xpath, path)  # 36氪报道 媒体报道 知名机构投资 消费生活人工智能便利店机械鲜食

                    path = "td[2]/span"; industry = cm.find_elment_by(ng_scope.find_element_by_xpath, path)#消费生活
                    path = "td[3]/span"; phase = cm.find_elment_by(ng_scope.find_element_by_xpath, path)#A+轮
                    path = "td[4]/span"; city = cm.find_elment_by(ng_scope.find_element_by_xpath, path)#广东省
                    path = "td[5]/span"; startDate = cm.find_elment_by(ng_scope.find_element_by_xpath, path)#2015-04

                    # ActionChains(driver).key_down(Keys.CONTROL).move_to_element(project_name).click(project_name).key_up(Keys.CONTROL).perform()
                    # ActionChains(driver) .click(project_name). perform()
                    time.sleep(0.5)
                    # project_name.click()
                    # String selectAll = Keys.chord(Keys.CONTROL, "a");
                    # driver.findElement(By.whatever("anything")).sendKeys(selectAll);
                    project = Project(logo_url = project_logoi.get_attribute("style"), name=project_namei.text,  industry = industry.text,
                                      financing_phase=phase.text, city=city.text, start_date=startDate.text, investment_platform = "rong.36kr.com")
                    if session.query(Project).filter(Project.name==project_namei.text, Project.investment_platform==pltfm_r36k).count() > 0:
                        logging.info(u'name:existed,skip. %s' ,  project_namei.text )
                        continue
                    session.add(project)
                    session.commit()
                    logging.info(u'logo[{logo}] name[{name}] intro[{intro}] tagi[{tagi}] industry[{industry}] phase[{phase}] city[{city}] startDate[{startDate}]'.format(
                                 logo = project_logoi.get_attribute("style"),
                                 name=project_namei.text,
                                 intro=project_intro_no_binding.text,
                                 tagi=project_tagi.text,
                                 industry=industry.text,
                                 phase=phase.text,
                                 city=city.text,
                                 startDate=startDate.text))
                    debug = True
                except:
                    traceback.print_exc()

            project_logo0 = ng_scope_ls[0].find_element(By.XPATH, "td[1]/a")
            project_logo0.click()
            # print x
            time.sleep(1.5) # Let the user actually see something!

            next_loop_exit = False
        # cloumn3ProjectList = driver.find_element_by_id("cloumn3ProjectList")
            path = "div#cloumn3ProjectList>ul>li.ng-scope"; ng_scope_ls= cm.find_elment_by(driver.find_elements_by_css_selector, path)
            for ng_scope in ng_scope_ls :
                try:
                    path = 'a'; project_logok = cm.find_elment_by(ng_scope.find_element_by_xpath, path)
                    project_logok.click(); time.sleep(2)
                    path = '//*[@id="node"]'; product_instro = cm.find_elment_by(ng_scope.find_element_by_xpath, path, using_txt=True,rtValWhnErr='') #项目介绍
                    # //*[@id="node"]
                    path =  '//*[@id="baseInfo"]/div/div[3]/div/div[1]/div/div[2]'; product_serv = cm.find_elment_by(ng_scope.find_element_by_xpath, path, using_txt=True,rtValWhnErr='') #产品服务
                    path = "div/p/span"; project_namek = cm.find_elment_by(ng_scope.find_element_by_xpath, path, using_txt=True,rtValWhnErr='')
                    if next_loop_exit:
                        logging.info(u'last project at this page, break loop. %s ',project_namek)
                        break
                    if project_name_last_text == project_namek:
                        next_loop_exit = True
                    d = {}
                    path = '//*[@id="projectHeader"]/div/div[2]/div/span/a'; project_sitek = cm.find_elment_by(driver.find_element_by_xpath, path, attribt='href',rtValWhnErr='')
                    d["site"]= project_sitek
                    d['introduction']=product_instro
                    d['product_description']=product_serv
                    d['logo_url']=project_logok.get_attribute("style")
                    if len(d) > 0:
                        session.query(Project).filter(Project.name==project_namek).update(d)
                        session.commit()
                        logging.info (u'update:project_namek[%s],project_logok[%s],product_instro[%s],product_serv[%s]', project_namek, project_logok.get_attribute("style"),product_instro ,product_serv  )
                    # 储存在数据库表里的id号, 作为融资经历、创始团队两个表的id
                    projectDB = session.query(Project).filter(Project.name == project_namek,
                                                              Project.investment_platform == pltfm_r36k).first()
                    projID = projectDB.id
                    # 融资经历
                    try:
                        project_history = driver.find_elements(By.XPATH, '//*[@id="financeHistory"]/div/div[2]/div[3]/ul/li')


                        logging.info(u'%d: %s' % (projID, project_namek))

                        for proj_hist in project_history:
                            inves_time = proj_hist.find_element(By.XPATH, 'div[1]').text
                            inves_turn = proj_hist.find_element(By.XPATH, 'div[2]/div[1]/span/a').text
                            inves_amount = proj_hist.find_element(By.XPATH, 'div[2]/div[1]/div[3]/div/span[2]').text
                            inves_man = proj_hist.find_element(By.XPATH, 'div[2]/div[1]/div[3]/div/div/div[2]/span').text

                            if session.query(Financing_phase).filter(Financing_phase.phase==inves_turn, Financing_phase.project_id == projID).count() > 0:
                                continue
                            fp = Financing_phase(phase=inves_turn, amount=inves_amount, investor=inves_man, date=inves_time, project_id=projID)
                            session.add(fp)
                            session.commit()
                            logging.info(u'financing history:\nphase: %s\tamount: %s\tinvestor:%s\tdate:%s\t' % (inves_turn, inves_amount,inves_man,inves_time))
                    except NoSuchElementException:
                        logging.info(u'no financing history:%s', project_namek)

                    # 创始团队
                    try:
                        project_team = driver.find_elements(By.XPATH, '//*[@id="founder"]/div/div[2]/div[1]/div[2]/table/tbody/tr')
                        for member in project_team:
                            member_name = member.find_element(By.XPATH, 'td[1]').text
                            member_pos = member.find_element(By.XPATH, 'td[2]').text
                            member_exp = member.find_element(By.XPATH, 'td[3]').text

                            if session.query(Company_member).filter(Company_member.name==member_name, Company_member.project_id == projID).count() > 0:
                                continue
                            commm = Company_member(name=member_name, position=member_pos, experience=member_exp, project_id=projID)
                            session.add(commm )
                            session.commit()
                            logging.info(u'project member:\nname: %s\tposition: %s' % (member_name, member_pos))
                    except NoSuchElementException:
                        logging.info(u'no financing history:%s', project_namek)
                    ActionChains(driver).move_to_element(project_logok). key_down( Keys.PAGE_DOWN).perform()
                    time.sleep(1)
                    ActionChains(driver).move_to_element(project_logok) .key_up(Keys.PAGE_DOWN).perform()
                    time.sleep(1)
                except:
                    traceback.print_exc()


        except:
            traceback.print_exc()

driver.close()
driver.quit()
session.close()
display.stop()