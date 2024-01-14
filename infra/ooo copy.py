from selenium import webdriver

# Chrome WebDriverのパスを指定します
driver_path = R"C:\Users\dobokuka4\Downloads\chromedriver_win32\chromedriver"

# Chrome WebDriverのオプションを指定します
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # ブラウザを表示しない場合はコメントアウトしてください

# WebDriverを起動します
driver = webdriver.Chrome(executable_path=driver_path, options=options)

# URLを指定してページを開きます
url = "https://www.mlit.go.jp/road/ir/ir-data/census_visualizationR3/index.html#13/35.6655/139.8296"
driver.get(url)

# クリックをシミュレートします（必要な場合）
driver.find_element_by_css_selector("body > div.ui-dialog.ui-widget.ui-widget-content.ui-corner-all.ui-draggable.ui-resizable").click()

# 指定したCSSセレクタの要素を取得します
element = driver.find_element_by_css_selector("#json_dlg > table > tbody > tr:nth-child(16) > td:nth-child(2)")

# 要素のテキストを表示します
print(element.text)

# WebDriverを終了します
driver.quit()