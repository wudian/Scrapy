
from selenium.webdriver.chrome.options import Options

db_connect_url = 'mysql+pymysql://test:test@192.168.27.210:3306/investment_platform_db?charset=utf8'

__options = Options()
__options.add_argument("--no-sandbox")
__options.add_argument("headless")
__chrome_options_no_sandbox_headless = __options


__options = Options()
__options.add_argument("--no-sandbox")
__chrome_options_no_sandbox = __options

chrome_options_using = __chrome_options_no_sandbox

class Account:
    def __init__(self, user, password):
        self.user = user
        self.password = password

account={}

account['rong.36kr.com'] = Account('15578826769','paSS2.718')
account['www.itjuzi.com'] = Account('xx','xxx')

pltfm_r36k = 'rong.36kr.com'