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

from shared.common.common import Cm, dct_list_push
from shared.common.common import generate_logger,set_dct
from shared.db.entity import Project, Financing_phase, Company_member, Shareholder
from shared.conf.itjuzi_conf import db_connect_url, account, pltfm_r36k, task_server_url, db_connect_url_bisz_table_id_start, \
    chrome_options_using,pltfm_itjuzi
from shared.util.util import get_system_uuid



WRITE_DB = False
LINUX = False
display = None
engine = None

driver = None
driver_cm = None

driver_song = None
song_cm = None

wrong_number = 0

engine = create_engine(db_connect_url)

DBSession = sessionmaker(bind=engine)
session = DBSession()
investment_platform = 'www.itjuzi.com'.encode('utf-8')
logging = generate_logger("tianyancha.log", "tianyancha")


def login():
    try:
        global driver
        global driver_cm
        global driver_song
        global song_cm
        if LINUX:
            driver = webdriver.Chrome(chrome_options=chrome_options_using)
            driver_song = webdriver.Chrome(chrome_options=chrome_options_using)
        else:
            driver_song = webdriver.Chrome()
            driver = webdriver.Chrome()
            
        driver.set_page_load_timeout(60)
        driver_song.set_page_load_timeout(60)
        driver_cm = Cm(logging, driver)
        song_cm = Cm(logging, driver_song)


        # driver.get('http://dt.baobao88.com/member/loginsta_index.php')
        driver_song.get('http://dt.baobao88.com/member/loginsta_index.php')
       
        # login_obj = driver_cm.find_elment_by_itjuzi(driver.find_element_by_class_name, 'login_nr')        
        # username = driver_cm.find_elment_by_itjuzi(login_obj.find_element_by_xpath, 'span/div[1]/input[6]')
        # password = driver_cm.find_elment_by_itjuzi(login_obj.find_element_by_xpath, 'span/div[2]/input')
        # submit = driver_cm.find_elment_by_itjuzi(login_obj.find_element_by_xpath, 'span/div[3]/input')
        # username.send_keys('wudian007')
        # password.send_keys('wudian123')
        # submit.click()
        # time.sleep(1)
        login_obj = song_cm.find_elment_by_itjuzi(driver_song.find_element_by_class_name, 'login_nr')        
        username = song_cm.find_elment_by_itjuzi(login_obj.find_element_by_xpath, 'span/div[1]/input[6]')
        password = song_cm.find_elment_by_itjuzi(login_obj.find_element_by_xpath, 'span/div[2]/input')
        submit = song_cm.find_elment_by_itjuzi(login_obj.find_element_by_xpath, 'span/div[3]/input')
        username.send_keys('wudian007')
        password.send_keys('wudian123')
        submit.click()
        time.sleep(1)
    except Exception as e:
        logging.exception('login fail')
        logging.exception(e)
        # if 'server detect i am machine' == e.message:
            # 'list' object has no attribute 'find_element_by_xpath'
            # ip被封了 重启vpn
            # sys.exit()


def get_from_one_page(url):
    global driver_song
    global driver
    global driver_cm
    global song_cm
    try:
        time.sleep(3)
        driver.get(url)
        time.sleep(3)
        path = 'div.list_right_nr1>ul'
        song_list = driver_cm.find_elment_by_itjuzi(driver.find_elements_by_css_selector, path)
        for song in song_list:
            path = 'li/a'
            url = driver_cm.find_elment_by_itjuzi(song.find_element_by_xpath, path, attribt='href', rtValWhnErr='')
            time.sleep(3)
            driver_song.get(url)

            name = song_cm.find_elment_by_itjuzi(driver_song.find_element_by_css_selector, 'div.t_mp3_info>h1', using_txt=True, rtValWhnErr='')
            ac_down = song_cm.find_elment_by_itjuzi(driver_song.find_element_by_class_name, 'ac_down')
            ac_down.click()
            url = song_cm.find_elment_by_itjuzi(driver_song.find_element_by_css_selector, 'div.content>iframe', attribt='src', rtValWhnErr='')
            print url
            time.sleep(3)
            driver_song.get(url)
            mp3 = song_cm.find_elment_by_itjuzi(driver_song.find_element_by_css_selector, 'div.dcl_bg>a', attribt='href', rtValWhnErr='')
            m = urllib2.urlopen(mp3)
            f = open("db/"+name+".mp3", "wb")
            f.write(m.read())
            f.close()

            # action = ActionChains(driver_song)
            # action.context_click(mp3)
            # time.sleep(1)
            # action.send_keys('k')
            # time.sleep(1)
            # action.send_keys(Keys.ENTER)            
            # action.perform()

    except Exception as e:
        logging.exception(e)

def get_from_pages():
    for i in range(1, 81):
        url = 'http://www.baobao88.com/bbmusic/eerge/16_%d.html' % i
        get_from_one_page(url)


if __name__ == '__main__':
    login()
    get_from_pages()

    driver.close()
    driver.quit()
    session.close()
    if LINUX:
        display.stop()

