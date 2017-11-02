# encoding: UTF-8
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import urllib
import traceback
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from shared.db.tree_entity import Project, News
from shared.common.common import generate_logger, Cm
from shared.conf.conf import chrome_options_using
from shared.conf.tree_conf import db_connect_url, chrome_options_using
import random
logging = generate_logger("info.log", "newsbaidu")
# logging.basicConfig(
# level=logging.INFO,
# format='%(asctime)s %(message)s',
# handlers=[logging.FileHandler("info.log"),
# logging.StreamHandler()])

updatemode = True

engine = create_engine(db_connect_url)
DBSession = sessionmaker(bind=engine)

session = DBSession()


# 从SQL数据库查询已有项目名称
# projectDB = session.query(Project).filter("id>:id").params(id=1).all()
projectDB = session.query(Project).filter(Project.id <10000).all()
# projectDB = session.query(Project).all()

# 设置浏览器
driver = webdriver.Chrome(chrome_options=chrome_options_using)
cm = Cm(logging, driver)
# driver2 = webdriver.Chrome(chrome_options=chrome_options_using)

wrong_number = 0
# 按项目名称作为关键词逐一查询
# for proj in projectDB:
for ii in range(0, len(projectDB)):
    print ii
    proj = projectDB[ii]
    keyword = proj.name
    keyword_id = proj.id
    logging.info('%d: %s \n' % (keyword_id, keyword))

    kw = keyword.encode('utf-8')

    # driver 搜关键词新闻
    driver.get('http://news.baidu.com/ns?word=' + kw + '&tn=news&from=news&cl=2&rn=20&ct=1')
    driver.set_page_load_timeout(60)
    time.sleep(random.randint(5, 10))  # Let the user actually see something!

    for nn in range(1,6):
        # node = driver1.find_elements(By.XPATH, '//*[@id="%d"]' % nn)
        path = '//*[@id="%d"]' % nn; node = cm.find_elment_by(driver.find_elements_by_xpath, path, rtValWhnErr='')
        # if node == '' or (type(node) is list and len(node)==1)
        if type(node) is list and len(node) > 0:
            path = 'h3/a'; news_url = cm.find_elment_by(node[0].find_element_by_xpath, path,attribt='href',rtValWhnErr='')
            path = 'h3/a'; news_title = cm.find_elment_by(node[0].find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
            path = 'div/p'; news_date = cm.find_elment_by(node[0].find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
            if news_date == '':
                path = 'div/div[2]/p'; news_date = cm.find_elment_by(node[0].find_element_by_xpath, path, using_txt=True, rtValWhnErr='')
            news_date = news_date[news_date.find(' ')+1:]
            logging.info('news_url: %s' % news_url)
            logging.info('news_title: %s' % news_title)
            logging.info('news_date: %s' % news_date)
            try:

                # 指向某一项目名称的数据条，判断是否已经存在
                dbCursor = session.query(News).filter(News.project_id == keyword_id, News.project_name == keyword, News.title == news_title)
                if dbCursor.count() == 0:
                    # print '正在保存新数据...'
                    logging.info(u'保存新数据...')
                    news = News(title = news_title, datetime = news_date, news_url = news_url, project_id=keyword_id, project_name=keyword)
                    session.add(news)
                    session.commit()
                elif updatemode:
                    logging.info(u'更新已保存数据')
                    dbCursor.update({"title": news_title, "datetime": news_date, "news_url": news_url, "project_id": keyword_id,"project_name": keyword})
                    session.commit()
                else:
                    logging.info(u'跳过已保存数据')

            except Exception as e:
                logging.exception(e)
                logging.error(u'出现错误')
                logging.error(e)
                driver.quit()
                time.sleep(5)
                driver = webdriver.Chrome(chrome_options=chrome_options_using)
                # wrong_number += 1
                # driver.get_screenshot_as_file('error_pic_driver1_%(wrong_number)d.png' % {'wrong_number': wrong_number})
                # traceback.print_exc()
        else:
            break
    logging.info(u'\n-----------完成----------\n')

session.close()
driver.quit()
# print '-----------完成----------'
logging.info(u'-----------完成----------');