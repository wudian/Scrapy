# -*- coding: utf-8 -*-
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from shared.db.entity import Project
from shared.conf.conf import db_connect_url, chrome_options_using
import time
import traceback
import logging
from shared.common.common import generate_logger,set_dct



logging = generate_logger("huxiu.log", "")

wrong_number = 1
def error2null(driver,func,*arg):
    try:
        return func(*arg)
    except Exception as e:
        global wrong_number 
        wrong_number += 1
        logging.info('something wrong and  at here')
        logging.info(e)
        driver.get_screenshot_as_file('error_pic%(wrong_number)d.png'%{'wrong_number':wrong_number})
        logging.info(u'错误图片已被存储为 error_pic%(wrong_number)d.png'%{'wrong_number':wrong_number})
        return 'null'


def major_page(driver,scope):
    '''
    从主详情页面抓取信息，返回基础信息以及子页面链接
    input:
        driver:主页面
        scope：模块
    '''
    project_name = error2null(driver,scope.find_element,By.XPATH, "a/h2").text
    #公司简介
    project_introduction = error2null(driver,scope.find_element,By.XPATH, "div[2]").text
    #所属行业
    project_industry = error2null(driver,scope.find_element,By.XPATH, "div[3]/ul/li[1]").text
    #所在城市
    project_city = error2null(driver,scope.find_element,By.XPATH, "div[3]/ul/li[2]").text
    #融资阶段
    project_wheel = error2null(driver,scope.find_element,By.XPATH, "div[3]/ul/li[3]").text
    #简介图片//*[@id="cy_center"]/div[3]/div[1]/div[1]/a/img
    pic_url = error2null(driver,scope.find_element,By.XPATH, "div[1]/a/img").get_attribute('src')
    #详情超链接： //*[@id="cy_center"]/div[3]/div[1]/div[1]/a
    details_url = error2null(driver,scope.find_element,By.XPATH, "div[1]/a").get_attribute('href')
    
    return pic_url,project_name,project_introduction,project_industry,project_wheel,project_city,details_url

def detail_page(details_url,debug=False):
    
    '''
    输入子页面url
    生辰新drive
    抓取信息//*[@id="cy_center"]/div[3]/div[1]/div[2]/div/div
    并在抓取完毕后关闭页面
    '''
    detail_driver = webdriver.Chrome(chrome_options=chrome_options_using)
    detail_driver.get(details_url)
    time.sleep(1)
    #产品简介
    product_description = error2null(detail_driver,detail_driver.find_element_by_id,'cy-cp-intro-warp').text
    #产品图片
    product_detail_img = error2null(detail_driver,detail_driver.find_elements_by_class_name,"gallery-img-box>li>img")
    product_detail_image_url = []
    for item in product_detail_img:
        image_url = error2null(detail_driver,item.get_attribute,'src')
        product_detail_image_url.append(image_url)
    #多个图片用 ; 隔开 提取的时候用判别式识别 分号；
    url_list = ';'.join(product_detail_image_url)
    #竞争优势
    product_advantage_list = error2null(detail_driver,detail_driver.find_elements_by_class_name,'cy-cp-advantage')
    product_advantage = product_advantage_list[0].text
    #产品成绩
    product_acheive = product_advantage_list[1].text
    #产品团队
    team_info = []
    product_team_list = error2null(detail_driver,detail_driver.find_elements_by_class_name,'cy-cp-team>li')
    for item in product_team_list:
        personal_name = error2null(detail_driver,detail_driver.find_element_by_class_name,'team-personnel-name').text
        job_position = error2null(detail_driver,detail_driver.find_element_by_class_name,'team-personnel-position').text
        person_intro = error2null(detail_driver,detail_driver.find_element_by_class_name,'team-personnel-intro').text
        info_list = [personal_name,job_position,person_intro]
        team_info.append(info_list)
    #创始人
    founder_name = team_info[0][0]
    founder_intro = team_info[0][2]
    #成立时间
    company_time = error2null(detail_driver,detail_driver.find_element_by_class_name,'company_time').text
    #融资进程/额度//*[@id="cy_center"]/div[3]/div[2]/div[1]/ul/li[3]/span
    raised_fund =  error2null(detail_driver,detail_driver.find_element_by_xpath,'//*[@id="cy_center"]/div[3]/div[2]/div[1]/ul/li[3]/span').text
    #公司名称//*[@id="company_name"]
    company_name = error2null(detail_driver,detail_driver.find_element_by_xpath,'//*[@id="company_name"]').text
    #公司网址
    company_weburl = error2null(detail_driver,detail_driver.find_element_by_xpath,'//*[@id="cy_center"]/div[3]/div[2]/div[1]/ul/li[2]/span/a').text
    time.sleep(1)
    detail_driver.close()
    output = (product_description,url_list,product_advantage,product_acheive,founder_name,founder_intro,company_time,raised_fund,company_name,company_weburl)
    if debug:
        print output
    return output



def input_scope(scope):
    
    test = major_page(driver, scope)
    sub_url = test[-1]
    test_sub = detail_page(sub_url)
    
    input_list = list(test[0:-1])
    input_list = input_list+list(test_sub)
    #project_name,project_introduction,project_industry,project_city,project_wheel,pic_url,
    df = pd.DataFrame(input_list, index=['logo_url','name','introductoin','industry',
                                            'financing_phase','city','product_description',
                                            'product_detail_image_url','product_advantage',
                                            'product_acheive','founder_name','founder_intro',
                                            'company_time','raised_fund','company_name','company_weburl'])
    df=df.T
    return df

def page_reader(scope_list):
    '''
    存储页面内所有
    '''
    for scope in scope_list:
        try:
            input_df = input_scope(scope)
            input_df['industry'] = map(lambda x:x[3:],input_df['industry'])    
            input_df['financing_phase'] = map(lambda x:x[5:],input_df['financing_phase'])   
            input_df['city'] = map(lambda x:x[4:],input_df['city'])      
            input_df['product_description'] = map(lambda x:x[4:],input_df['product_description'])       
            input_df = list(input_df.iloc[0,:])
            huxiu = Project(logo_url = input_df[0],
                          name=input_df[1], 
                          introduction=input_df[2], 
                          industry = input_df[3],
                          financing_phase=input_df[4],
                          city=input_df[5],
                          product_description = input_df[6],
                          picture_set = input_df[7],
                          advantage = input_df[8],
                          achievement = input_df[9],
                          founder = input_df[10],
                          founder_description = input_df[11],
                          start_date = input_df[12],
                          raised_fund = input_df[13],
                          company_name = input_df[14],
                          site = input_df[15],
                          investment_platform = 'www.huxiu.com')
            if session.query(Project).filter(Project.name ==huxiu.name, Project.investment_platform=='www.huxiu.com').count() >0 :
                logging.info(u'已有,跳过: %(name)s'%{'name':huxiu.name})
                continue
            session.add(huxiu)
            session.commit()
            logging.info(u'成功抓取并写入: %(name)s'%{'name':input_df[1]})
        except Exception as e:
            logging.info(u'数据库存储错误')
            traceback.print_exc()
            logging.info(e)  
            
            
engine = create_engine(db_connect_url)
DBSession = sessionmaker(bind=engine)
session = DBSession()

driver = webdriver.Chrome()#chrome_options=chrome_options_using
driver.get("https://www.huxiu.com/chuangye")
for i in range(300):
    scope_list = driver.find_elements(By.CSS_SELECTOR,".cy-cp-box.transition")
    page_reader(scope_list)
    driver.execute_script('document.querySelectorAll("div.cy-cp-box.transition").forEach(function (i){  i.remove();})    ')
    next_page_button = driver.find_element_by_xpath('//*[@id="cy_center"]/div[5]')
    next_page_button.click()
    driver.implicitly_wait(5)  
          
        
driver.close()
"""
df['industry'] = map(lambda x:x[3:],df['industry'])    
df['financing_phase'] = map(lambda x:x[5:],df['financing_phase'])   
df['city'] = map(lambda x:x[4:],df['city'])      
df['product_description'] = map(lambda x:x[4:],df['product_description'])        
dbconfig = {
        'user':'test',
        'password':'test', 
        'schema':'investment_platform_db', 
        'host':'192.168.27.210', 
        'port':3306
         }
connection = connect(**dbconfig)

#写入数据
insert_keys = ['logo_url','name','introduction','industry','financing_phase','city','product_description','picture_set',
               'advantage','achievement','founder','founder_description','start_date','raised_fund','company_name','site','investment_platform']
for i in range(len(df)):
    insert_values=list(df.iloc[i,:])
    insertkey = ','.join(insert_keys)
    insert_values.append("https://www.huxiu.com/chuangye")
    insert_values = map(lambda x: '"'+x+'"',insert_values)
    insert_values = ','.join(insert_values)
    strdic = {
            'table_name':'huxiu',
            'columns':str(insertkey),
            'values':insert_values
            }
    query = 'INSERT INTO %(table_name)s (%(columns)s) VALUES (%(values)s)'%strdic
    connection.execute(query)
    """