# encoding: UTF-8
from selenium.webdriver.chrome.options import Options

# db_connect_url = 'mysql+pymysql://root:root@localhost:3306/investment_platform_db?charset=utf8'
# db_connect_url = 'mysql+pymysql://dev:dev.0.o-_->>>@10.253.115.203:3306/investment_platform_db?charset=utf8'   # 开发环境数据库
db_connect_url = 'mysql+pymysql://dev:dev.0.o-_->>>@localhost:3306/investment_platform_db?charset=utf8'   # 开发环境数据库
db_connect_url_bisz_table_id_start = 'mysql+pymysql://root:root@localhost:3306/investment_platform_db{bisz_table_id_start}?charset=utf8'
db_connect_url4init = 'mysql+pymysql://root:root@localhost:3306/test?charset=utf8'

# db_connect_url = 'mysql+pymysql://root:root@localhost:3306/investment_platform_db?charset=utf8'
# db_connect_url_bisz_table_id_start = 'mysql+pymysql://root:root@localhost:3306/investment_platform_db{bisz_table_id_start}?charset=utf8'
# db_connect_url4init = 'mysql+pymysql://root:root@localhost:3306/test?charset=utf8'

task_server_url = 'http://150.95.157.93:8000'

__options = Options()
__options.add_argument("headless")
__options.add_argument("--lang=zh")
# __options.binary_location = '/usr/bin/google-chrome-stable'
__chrome_options_headless = __options

__options = Options()
__options.add_argument("--no-sandbox")
__chrome_options_no_sandbox = __options

__options = Options()
__chrome_options_sandbox = __options

chrome_options_using = __chrome_options_sandbox

class Account:
    def __init__(self, user, password):
        self.user = user
        self.password = password

account={}

# account['rong.36kr.com'] = Account('proooogram@outlook.com','paSS2.718')
account['rong.36kr.com'] = Account('shcaoguilin@sina.com','paSS2.718')
account['www.itjuzi.com'] = Account('xx','xxx')
account['www.innotree.cn'] = Account('18616858682','123456')
pltfm_r36k = 'rong.36kr.com'

pltfm_tree = 'www.innotree.cn'