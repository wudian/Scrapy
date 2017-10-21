# -*- coding: utf-8 -*-
import logging
import logging.handlers
import traceback

import datetime


def set_dct(dct,k,v):
    dct[k] = v
    return True

def dct_list_push(dct,k,v):
    if dct.has_key(k):
        dct[k].append(v)
    else:
        dct[k] = [v]
    return True


def generate_logger(log_file_name,tag):

    logger = logging.getLogger(tag)
    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setFormatter( logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s") )
    logger.addHandler(ch)

    fh = logging.handlers.RotatingFileHandler(log_file_name, maxBytes=32 * 1024 * 1024, backupCount=5)
    fh.setFormatter( logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s") )
    logger.addHandler(  fh )

    return logger



wrong_number = 1
def error2null(driver,func,*arg):
    try:
        x= func(*arg)
        return x
    except Exception as e:
        global wrong_number
        wrong_number += 1
        logging.info('something wrong and  at here')
        logging.info(e)
        driver.get_screenshot_as_file('error_pic%(wrong_number)d.png'%{'wrong_number':wrong_number})
        logging.info(u'错误图片已被存储为 error_pic%(wrong_number)d.png'%{'wrong_number':wrong_number})
        return 'null'

class Cm:
    def s2int(self, s,rtValWhnErr=None):
        try:
            i = int(s)
            return i
        except:
            return rtValWhnErr
    def __init__(self,logger,driver):
        self.logger = logger
        self.driver = driver
        self.continue_error  = 0
    def find_elment_by(self, find_element_func, path1, using_txt = False, attribt = None, rtValWhnErr = None):
        try:
            elem= find_element_func(path1)
            self.continue_error = 0
            if using_txt:
                txt = elem.text
                if len(txt) == 0:
                    return rtValWhnErr
                return txt
            if attribt is not None:
                attrb = elem.get_attribute(attribt)
                return attrb
            return elem
        except Exception as e:
            self.continue_error = self.continue_error + 1
            if self.continue_error > 9:
                raise Exception('server detect i am machine')
            traceback.print_exc()
            dt = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            self.driver.get_screenshot_as_file('error%s.png'%dt)
            return rtValWhnErr

    def find_elment_by_itjuzi(self, find_element_func, path1, using_txt = False, attribt = None, rtValWhnErr = None):
        try:
            elem= find_element_func(path1)
            self.continue_error = 0
            if using_txt:
                txt = elem.text
                if len(txt) == 0:
                    return rtValWhnErr
                return txt
            if attribt is not None:
                attrb = elem.get_attribute(attribt)
                return attrb
            return elem
        except Exception as e:
            self.continue_error = self.continue_error + 1
            if self.continue_error > 9:
                raise Exception('server detect i am machine')
            return rtValWhnErr