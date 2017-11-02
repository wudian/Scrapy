# coding=utf-8
import time
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from shared.common.common import error2null,generate_logger
from shared.db.entity import Project,Financing_phase
from shared.conf.conf import db_connect_url,chrome_options_using


logging = generate_logger("info.log", "cyzone")
engine = create_engine(db_connect_url)
DBSession = sessionmaker(bind=engine)
session = DBSession()
# driver = webdriver.Chrome(chrome_options=chrome_options_using)
# detail_driver = webdriver.Chrome(chrome_options=chrome_options_using)
driver = webdriver.Chrome()
time.sleep(5)
detail_driver = webdriver.Chrome()

def login():
    driver.get('http://www.cyzone.cn/member/index/login')
    detail_driver.get('http://www.cyzone.cn/member/index/login')
    time.sleep(1) # Let the user actually see something!

    username = detail_driver.find_element_by_name('email')
    password = detail_driver.find_element_by_css_selector('[id=reg-passwd]')
    submit = detail_driver.find_element_by_class_name('submit-btn')
    username.send_keys('990896286@qq.com')
    password.send_keys('881124')
    submit.click()
    time.sleep(1)

    username = driver.find_element_by_name('email')
    password = driver.find_element_by_css_selector('[id=reg-passwd]')
    submit = driver.find_element_by_class_name('submit-btn')
    username.send_keys('990896286@qq.com')
    password.send_keys('881124')
    submit.click()
    time.sleep(1)

login()


for i in range(200,230):

    driver.get('http://www.cyzone.cn/vcompany/list-0-0-%d/' % i)
    plate_item_ls = driver.find_elements(By.CSS_SELECTOR, "tr.table-plate.item")
    for n in range(1, len(plate_item_ls)):
        try:
            plate_item = plate_item_ls[n]

            project_image_src = error2null(driver, plate_item.find_element, By.XPATH, "td[1]/a/img").get_attribute("src")
            project_name = error2null(driver, plate_item.find_element, By.XPATH, "td[2]/a").text
            project_stage = error2null(driver, plate_item.find_element, By.XPATH, "td[3]").text
            project_type = error2null(driver, plate_item.find_element, By.XPATH, "td[4]/a").text
            project_time = error2null(driver, plate_item.find_element, By.XPATH, "td[5]").text

            logging.info(' %s %s %s %s %s', project_image_src, project_name, project_stage, project_type, project_time)

            # turn to detail page
            detail_btn = plate_item.find_element(By.XPATH, "td[2]/a")
            detail_url = detail_btn.get_attribute('href')
            detail_driver.get(detail_url)
            time.sleep(2)
            # time.sleep(3)

            company_logo = error2null(detail_driver, detail_driver.find_element, By.XPATH, '//*[@id="main"]/div[3]/div[1]/div/div/img').get_attribute("src")
            company_full_name = error2null(detail_driver, detail_driver.find_element, By.XPATH, '//*[@id="main"]/div[3]/div[1]/ul/li[2]').text
            company_website = error2null(detail_driver, detail_driver.find_element, By.XPATH, '//*[@id="main"]/div[3]/div[1]/ul/li[3]/div[1]/a').text
            registered_location = error2null(detail_driver, detail_driver.find_element, By.XPATH, '//*[@id="main"]/div[4]/div/div[2]/div[1]/div[2]/ul/li[2]/span/a').text
            brief_intro = error2null(detail_driver, detail_driver.find_element, By.XPATH,'//*[@id="main"]/div[4]/div/div[2]/div[1]/div[3]/div').text

            logging.info ('%s %s %s',company_full_name, registered_location, brief_intro)

            dbCursor = session.query(Project).filter(Project.name == project_name,
                                                     Project.investment_platform == 'www.cyzone.cn')
            project = dbCursor.first()
            if dbCursor.count()==0:
                project = Project(logo_url=project_image_src,
                                  name=project_name,
                                  financing_phase=project_stage,
                                  industry=project_type,
                                  start_date=project_time,
                                  introduction=brief_intro,
                                  city=registered_location,
                                  company_name=company_full_name,
                                  site=company_website,
                                  investment_platform="www.cyzone.cn")
                # if session.query(Project).filter(Project.name == project_name, Project.investment_platform == 'www.cyzone.cn').count() > 0:
                #     # if dbCursor.count() > 0:
                #     #     dbCursor.update({"financing_phase": project_stage})
                #     #     session.commit()
                #     # logging.info(u'name:existed,skip. %s', project_name)
                #     # # continue
                session.add(project)
                session.commit()
            else:
                dbCursor.update(
                    {"logo_url": project_image_src, "name": project_name, "introduction": brief_intro,
                     "industry": project_type, "city": registered_location, "financing_phase": project_stage,
                     "company_name":company_full_name,
                     "site": company_website, "investment_platform": "www.cyzone.cn"})
                session.commit()

            financing_experience_ls=error2null(detail_driver,detail_driver.find_elements,By.CSS_SELECTOR,"div.live>table>tbody>tr")
            for ii in range(1,len(financing_experience_ls)):
                financing = financing_experience_ls[ii]
                try:
                    financing_stage=error2null(detail_driver,financing.find_element, By.XPATH,'td[1]').text
                    financing_amount=error2null(detail_driver,financing.find_element, By.XPATH,'td[2]').text
                    investor=error2null(detail_driver,financing.find_element, By.XPATH,'td[3]').text
                    financing_time=error2null(detail_driver,financing.find_element, By.XPATH,'td[4]').text
                    if u'登录' in financing_stage:
                        login()
                        detail_driver.get(detail_url)
                        driver.get('http://www.cyzone.cn/vcompany/list-0-0-%d/' % i)
                        detail_driver.implicitly_wait(3)
                        continue
                    logging.info('%s %s %s %s',financing_stage, financing_amount, investor, financing_time)
                    # if session.query(Financing_phase).filter(Financing_phase.phase == financing_stage,
                    #                                          Financing_phase.project_id == project.id).count() > 0:
                       # continue
                    dbCursor = session.query(Financing_phase).filter(Financing_phase.phase == financing_stage,
                                                                     Financing_phase.project_id == project.id)
                    if dbCursor.count() == 0:
                        fp = Financing_phase(phase=financing_stage,
                                             amount=financing_amount,
                                             investor=investor,
                                             date=financing_time,
                                             project_id=project.id,
                                             investment_platform="www.cyzone.com")
                        session.add(fp)
                        session.commit()
                    else:
                        dbCursor.update({"phase": financing_stage, "amount":financing_amount, "investor": investor, "date": financing_time,
                                         "project_id": project.id, "investment_platform":"www.cyzone.com"})
                        session.commit()
                except:
                    traceback.print_exc()


        except:
            traceback.print_exc()
            driver.get_screenshot_as_file('driver.png')
            detail_driver.get_screenshot_as_file('detail_driver.png')


            debug = True
