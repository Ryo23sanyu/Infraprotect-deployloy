import requests
from bs4 import BeautifulSoup

url = "https://www1.mlit.go.jp/road/ir/ir-data/census_visualizationR3/index.html#15/35.6378/139.6306"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
# 例: 「昼間１２時間交通量（全車上下計）（台）」というテキストを持つ要素を探す
target_element = soup.select_one("#json_dlg > table > tbody > tr:nth-child(16) > td:nth-child(2)")
print(target_element)