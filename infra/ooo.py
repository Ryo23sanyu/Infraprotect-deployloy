from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import signal
import webbrowser

try:  
  url = 'https://www.google.co.jp/maps/@35.8803435,140.5045137,13'
  google = webbrowser.open(url, new=0, autoraise=True)

  # 要素のサイズを取得
  element = google.find_element_by_tag_name('body')
  size = element.size

  # 要素の位置を取得
  location = element.location

  # 要素の中心点を計算
  center_x = location['x'] + size['width'] / 2
  center_y = location['y'] + size['height'] / 2

  # 中心点をクリック
  actions = webdriver.ActionChains(google)
  actions.move_to_element_with_offset(element, center_x, center_y)
  actions.click()
  actions.perform()

finally:
  os.kill(google.service.process.pid,signal.SIGTERM)
