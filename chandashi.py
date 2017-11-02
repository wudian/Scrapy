# encoding: UTF-8
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import urllib
import traceback
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from shared.db.entity import Project, Chandashi_rank
from shared.common.common import generate_logger
from shared.conf.conf import chrome_options_using
from shared.conf.tree_conf import db_connect_url

logging = generate_logger("info.log", "chandashi")
# logging.basicConfig(
# level=logging.INFO,
# format='%(asctime)s %(message)s',
# handlers=[logging.FileHandler("info.log"),
# logging.StreamHandler()])

updatemode = False

engine = create_engine(db_connect_url)
DBSession = sessionmaker(bind=engine)

session = DBSession()


# 从SQL数据库查询已有项目名称
projectDB = session.query(Project).all()

# 设置浏览器
driver1 = webdriver.Chrome(chrome_options=chrome_options_using)
# driver1.set_page_load_timeout(3)
driver2 = webdriver.Chrome(chrome_options=chrome_options_using)
# driver2.set_page_load_timeout(3)
wrong_number = 0
# 按项目名称作为关键词逐一查询
# for proj in projectDB:
for ii in range(38600,len(projectDB)):
    print ii
    proj = projectDB[ii]
    keyword = proj.name
    keyword_id = proj.id
    logging.info('%d: %s \n' % (keyword_id, keyword))
    dbCursor = session.query(Chandashi_rank).filter(Chandashi_rank.project_id == keyword_id)
    if not updatemode and dbCursor.count() > 0:
        logging.info(u'跳过已保存数据')
        continue
    try:
        param={}
        param['keyword'] = keyword.encode('utf-8')
        kw = urllib.urlencode(param)

        # driver1 搜关键词热度
        # driver1.get('https://www.chandashi.com/search/index.html?keyword=%E9%9A%8F%E6%89%8B%E8%AE%B0&type=store')
        driver1.get('https://www.chandashi.com/search/index.html?' + kw + '&type=store')
        driver1.set_page_load_timeout(60)
        time.sleep(0.5) # Let the user actually see something!
        #driver.implicitly_wait(10)

        # node1 = driver1.find_elements(By.CSS_SELECTOR, '.col-lg-2.col-md-1.col-sm-1.text-center')
        # hotindextext = node1[0].text
        node2 = driver1.find_elements(By.XPATH, '//*[@id="pageTop"]/section/div[1]/table/tbody/tr[2]/td[2]/a')
        if len(node2)==0:
            # print(' 关键词无热度！')
            logging.warning(u'关键词无热度')
            hotindex = None
        else:
            # print('关键词热度：')

            hotindex = int(node2[0].text)
            # print hotindex
            logging.info(u'关键词热度:%s' % hotindex)

        # time.sleep(0.5) # Let the user actually see something!

        # 进入第一条app详情页面查排名
        # node3 = driver1.find_elements(By.XPATH, '//*[@id="searchlist"]')
        item = driver1.find_elements(By.XPATH, '//*[@id="searchlist"]/div[1]/div/a')
        if len(item)==0:
            # print('没有对应的app!')
            logging.warning(u'没有对应的app')
            appname = None
            ranktype1 = None
            ranktype2 = None
            rank1 = None
            rank2 = None
        else:
            appname = item[0].get_attribute('title')
            url2 = item[0].get_attribute('href')

        # # driver2 两个排名

            driver2.get(url2)
            driver2.set_page_load_timeout(60)
            time.sleep(0.5)

            node3 = driver2.find_elements(By.CSS_SELECTOR, ".col-xs-4.text-center.gray-th")
            ranktype1 = node3[1].text
            ranktype2 = node3[2].text


            node4 = driver2.find_elements(By.XPATH, '//*[@id="main-content"]/div/div[2]/table/tbody/tr[2]/td[2]')
            rank1 = node4[0].text
            node5 = driver2.find_elements(By.XPATH, '//*[@id="main-content"]/div/div[2]/table/tbody/tr[2]/td[3]')
            rank2 = node5[0].text

            # print appname
            # print ranktype1
            # print rank1
            # print ranktype2
            # print rank2
            logging.info('appname: %s \n %s: %s \n %s: %s' % (appname, ranktype1, rank1, ranktype2, rank2))

        # 指向某一项目名称的数据条，判断是否已经存在
        # dbCursor = session.query(Chandashi_rank).filter(Chandashi_rank.project_id == keyword_id)
        if dbCursor.count() == 0:
            # print '正在保存新数据...'
            logging.info(u'保存新数据...')
            chandashi_rank = Chandashi_rank(project_id=keyword_id, name=keyword, appname=appname, hotindex=hotindex, ranktype1=ranktype1, rank1=rank1, ranktype2=ranktype2, rank2=rank2)
            session.add(chandashi_rank)
            session.commit()
        else:
            logging.info(u'跳过已保存数据')
            # logging.info(u'更新已保存数据')
            # dbCursor.update({"name": keyword, "appname": appname, "hotindex": hotindex, "ranktype1": ranktype1, "rank1": rank1, "ranktype2": ranktype2, "rank2": rank2})
            # session.commit()
        logging.info(u'\n-----------完成----------\n')
    except Exception as e:
        logging.error(u'出现错误')
        logging.error(e)
        driver1.quit()
        driver2.quit()
        driver1 = webdriver.Chrome(chrome_options=chrome_options_using)
        driver2 = webdriver.Chrome(chrome_options=chrome_options_using)
        wrong_number += 1
        driver1.get_screenshot_as_file('error_pic_driver1_%(wrong_number)d.png' % {'wrong_number': wrong_number})
        driver2.get_screenshot_as_file('error_pic_driver2_%(wrong_number)d.png' % {'wrong_number': wrong_number})
        # traceback.print_exc()


session.close()
driver1.quit()
driver2.quit()
# print '-----------完成----------'
logging.info(u'-----------完成----------')