
from selenium.webdriver.chrome.options import Options

db_connect_url = 'mysql+pymysql://root:root@localhost:3306/investment_platform_db?charset=utf8'
db_connect_url_bisz_table_id_start = 'mysql+pymysql://root:root@localhost:3306/investment_platform_db{bisz_table_id_start}?charset=utf8'
db_connect_url4init = 'mysql+pymysql://root:root@localhost:3306/test?charset=utf8'

# db_connect_url = 'mysql+pymysql://root:root@localhost:3306/investment_platform_db?charset=utf8'
# db_connect_url_bisz_table_id_start = 'mysql+pymysql://root:root@localhost:3306/investment_platform_db{bisz_table_id_start}?charset=utf8'
# db_connect_url4init = 'mysql+pymysql://root:root@localhost:3306/test?charset=utf8'

task_server_url = 'http://task_manager:8000'

__options = Options()
__options.add_argument("headless")
__chrome_options_headless = __options

chrome_options_using = __chrome_options_headless

class Account:
    def __init__(self, user, password):
        self.user = user
        self.password = password

account={}

# account['rong.36kr.com'] = Account('proooogram@outlook.com','paSS2.718')
account['rong.36kr.com'] = Account('shcaoguilin@sina.com','paSS2.718')
account['www.itjuzi.com'] = Account('xx','xxx')

pltfm_r36k = 'rong.36kr.com'
pltfm_itjuzi = 'www.itjuzi.com'
