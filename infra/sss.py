from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# ブラウザのインスタンスを作成
driver = webdriver.Chrome()

# 新しいウィンドウを開く
driver.execute_script("window.open('about:blank', 'new_window')")

# 新しいウィンドウのハンドルを取得
new_window_handle = driver.window_handles[-1]

# 新しいウィンドウに切り替える
driver.switch_to.window(new_window_handle)

# 表示したいページのURLを指定
driver.get('https://www.google.co.jp/maps')

# 要素のサイズを取得
element = driver.find_element_by_tag_name('body')
size = element.size

# 要素の位置を取得
location = element.location

# 要素の中心点を計算
center_x = location['x'] + size['width'] / 2
center_y = location['y'] + size['height'] / 2

# 中心点をクリック
actions = webdriver.ActionChains(driver)
actions.move_to_element_with_offset(element, center_x, center_y)
actions.click()
actions.perform()

# ブラウザを終了
driver.quit()