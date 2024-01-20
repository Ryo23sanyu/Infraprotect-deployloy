import webbrowser
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome import service as sv
import math, pyautogui

url = 'https://www.mlit.go.jp/road/ir/ir-data/census_visualizationR3/index.html#16/35.7223/140.0734'
webbrowser.open(url, new=1, autoraise=True)

# (100, 200)の位置にマウスカーソルを移動
pyautogui.moveTo(764,358)

# クリック
pyautogui.click()