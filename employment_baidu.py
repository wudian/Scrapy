# coding=utf-8
import time
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from shared.common.common import generate_logger,Cm
from shared.db.entity import Project,Employment
from shared.conf.conf import db_connect_url,db_connect_url_public,chrome_options_using
import random



# chrome_options = webdriver.ChromeOptions()
logging = generate_logger("info.log", "employment_baidu")

updatemode = True

engine = create_engine(db_connect_url_public)
DBSession = sessionmaker(bind=engine)
session_public = DBSession()

engine2 = create_engine(db_connect_url)
DBSession = sessionmaker(bind=engine2)
session = DBSession()

projectDB = session_public.query(Project).filter(Project.company_id<10000).all()
session_public.close()
# driver = webdriver.Chrome(chrome_options=chrome_options_using)
driver = webdriver.Chrome()
detail_driver = webdriver.Chrome()
cm = Cm(logging, driver)

wrong_number = 0

for i in range(0, len(projectDB)):
    print i
    proj = projectDB[i]
    keyword = proj.company_name
    keyword_id = proj.company_id
    investment_platform= proj.investment_platform
    project_name=proj.name
    logging.info('%d: %s \n' % (keyword_id, keyword))

    kw = keyword.encode('utf-8')
    driver.get("http://zhaopin.baidu.com/quanzhi?query=" + kw )
    driver.set_page_load_timeout(60)
    time.sleep(random.randint(1, 10))

    job_ls = driver.find_elements(By.CSS_SELECTOR, "a.clearfix.item.line-bottom")

    for n in range(0, len(job_ls)):
        try:
            job_item = job_ls[n]
            path="div[1] / div /span"; job_name = cm.find_elment_by(job_item.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
            path="div[1]/p"; job_company = cm.find_elment_by(job_item.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
            job_company =job_company[job_company.rindex(' '):len(job_company)]
            # path ="div[2]/p[2]"; datetime = cm.find_elment_by(job_item.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
            # datetime=datetime[0:datetime.index('| ')]
            # datetime=datetime[:-2]
            path ="div[2] / p[1]"; salary = cm.find_elment_by(job_item.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
            path ="div[1]/p"; location = cm.find_elment_by(job_item.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
            location=location[0:location.index('| ')]
            path ="div[2]/p[2]"; origin= cm.find_elment_by(job_item.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
            origin=origin[origin.rindex(' '):len(origin)]
            origin=origin[3:len(origin)]

            logging.info(' %s %s %s %s %s ', job_name, job_company, salary, location, origin)
            # logging.info(' %s %s %s %s %s %s ', job_name, job_company, salary, location, origin,datetime)

            # path="//*[@id='feed-list']/a"; detail_btn = cm.find_elment_by(job_item.find_element_by_xpath, path)
            # detail_url = detail_btn.get_attribute('href')
            detail_url = job_item.get_attribute('href')
            detail_driver.get(detail_url)
            time.sleep(1)


            path = "/html/body/div[3]/div[1]/div[4]/div[1]/div/div/div[1]/div/p[2]"; datetime = cm.find_elment_by(detail_driver.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
            datetime = datetime[5:len(datetime)]
            if len(datetime)>11:
                # datetime=job_category
                path = "/html/body/div[3]/div[1]/div[4]/div[1]/div/div/div[1]/div/p[1]";datetime = cm.find_elment_by(detail_driver.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
                datetime = datetime[5:len(datetime)]

            path = "/html/body/div[3]/div[1]/div[4]/div[1]/div/div/div[1]/div/p[1]";
            job_category = cm.find_elment_by(detail_driver.find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
            job_category = job_category[5:len(job_category)]
            if (job_category.find(datetime)!=-1):
                job_category="N/A"

            logging.info('%s %s', job_category, datetime)
            # logging.info('%s ', job_category)

            try:

                #指向某一项目名称的数据条，判断是否已经存在
                dbCursor = session.query(Employment).filter(Employment.company_id == keyword_id, Employment.company_name ==job_company ,Employment.job_category==job_category,Employment.investment_platform==investment_platform,
                                                            Employment.job_desc == job_name, Employment.salary== salary, Employment.datetime==datetime, Employment.job_source==origin, Employment.address==location, Employment.project_name==project_name)
                if dbCursor.count() == 0:
                    # print '正在保存新数据...'
                    logging.info(u'保存新数据...')
                    job = Employment(job_desc=job_name, company_name=job_company,datetime=datetime, salary=salary, job_source=origin, address=location, company_id=keyword_id,
                                     job_category =job_category, investment_platform = investment_platform,project_name=project_name)
                    session.add(job)
                    session.commit()
                elif updatemode:
                    logging.info(u'更新已保存数据')
                    dbCursor.update(
                        {"job_desc":job_name, "company_name":job_company,"datetime":datetime, "salary":salary, "job_source":origin,"address":location,"company_id":keyword_id,
                         "job_category":job_category, "investment_platform":investment_platform,"project_name":project_name})
                    session.commit()
                else:
                    logging.info(u'跳过已保存数据')

            except Exception as e:
                logging.exception(e)
                logging.error(u'出现错误')
                logging.error(e)
                driver.quit()
                time.sleep(5)
                driver = webdriver.Chrome()
                # wrong_number += 1
                # driver.get_screenshot_as_file('error_pic_driver1_%(wrong_number)d.png' % {'wrong_number': wrong_number})
                # traceback.print_exc()


        except:
            traceback.print_exc()


session.close()
driver.quit()
detail_driver.quit()
# print '-----------完成----------'
logging.info(u'-----------完成----------');

