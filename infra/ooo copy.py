from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome import service as sv
import math

# Chrome WebDriverのパスを指定します
# executable_path = "chromedriver.exe"
executable_path = R"C:\work\django\myproject\myvenv\Infraproject\infraproject\chromedriver-win64\chromedriver.exe"
chrome_service = sv.Service(executable_path=executable_path)

# Chrome WebDriverのオプションを指定します
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # ブラウザを表示しない場合はコメントアウトしてください

# WebDriverを起動します
driver = webdriver.Chrome(service=chrome_service, options=options)

# URLを指定してページを開きます
url = "https://www.google.co.jp/maps"
driver.get(url)

