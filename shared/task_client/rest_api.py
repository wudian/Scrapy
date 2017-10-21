# -*- coding: utf-8 -*-
import logging
import logging.handlers
import traceback

import datetime


class TaskRestClient:
    def __init__(self,task_server_url):
        self.task_server_url = task_server_url

    def get_platform_account(self,investment_platform):
        url_get_platform_account = '{task_server_url}/get_platform_account/{investment_platform}'.format(
            investment_platform=investment_platform, task_server_url=self.task_server_url)
        resp_get_platform_account = json.load(urllib2.urlopen(url_get_platform_account))
        usernameI = resp_get_platform_account['username']
        passwordI = resp_get_platform_account['pass']
        logging.info("platform,username[{username},password[{password}]]".format(password=passwordI,username=usernameI))
        return (usernameI,passwordI)

    def assign_worker_id(self,system_uuid):
        url_get_worker_id = '{task_server_url}/assign_worker_id/{worker_system_uuid}'.format(
            worker_system_uuid=system_uuid, task_server_url=self.task_server_url)
        resp_get_worker_id = json.load(urllib2.urlopen(url_get_worker_id))
        worker_id = resp_get_worker_id['worker_id']
        bisz_table_id_start = resp_get_worker_id['bisz_table_id_start']
        return (worker_id, bisz_table_id_start)

    def allocate_task(self,worker_id, investment_platform):
        url_get_task = '{task_server_url}/allocate_task/{worker_id}/{investment_platform}'.format(worker_id=worker_id,
                                                                                                  investment_platform=investment_platform,
                                                                                                  task_server_url=task_server_url)
        resp_get_task = json.load(urllib2.urlopen(url_get_task))
        url_ls = [i['entrance_url'] for i in resp_get_task]
        return url_ls
