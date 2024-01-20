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
url = "https://www.mlit.go.jp/road/ir/ir-data/census_visualizationR3/index.html#13/35.7486/140.1799"
driver.get(url)

# セレクターを使用して要素を取得
element = driver.find_element_by_css_selector("#json_dlg > table > tbody > tr:nth-child(16) > td:nth-child(2)")

# 要素の位置とサイズを取得
element_location = element.location
element_size = element.size

# 要素の中央の座標を計算
center_x = element_location['x'] + math.floor(element_size['width'] / 2)
center_y = element_location['y'] + math.floor(element_size['height'] / 2)

# クリックする処理
actions = ActionChains(driver)
actions.move_by_offset(center_x, center_y).click().perform()

# クリックをシミュレートします（必要な場合）
# driver.find_element_by_css_selector("body > div.ui-dialog.ui-widget.ui-widget-content.ui-corner-all.ui-draggable.ui-resizable").click()

# 指定したCSSセレクタの要素を取得します
element = driver.find_element_by_css_selector("#json_dlg > table > tbody > tr:nth-child(16) > td:nth-child(2)")

# 要素のテキストを表示します
print(element.text)

# WebDriverを終了します
driver.quit()