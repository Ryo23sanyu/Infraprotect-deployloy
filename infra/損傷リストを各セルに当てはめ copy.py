from itertools import zip_longest
import re
import openpyxl
from openpyxl.drawing.image import Image
import os

# データ (サンプル)
data = [
    {'this_time_picture': ['infra\img\9月7日　佐藤　地上\P9070422.JPG']}
]


# 指定したエクセルファイルを開く
wb = openpyxl.load_workbook('C:\work\django\myproject\program\Infraproject\macro.xlsx')
ws = wb['sheet1']  # シート名を指定

# セル位置のリストを生成 ↓
picture_cell_positions = [] # 損傷写真

join_picture_cell_positions = ['E13', 'AE13', 'BE13']
# セル位置のリストを生成 ↑

# 最大の写真サイズ（幅、高さ）
max_width, max_height = 240, 180 # 4:3

# 位置を追跡するカウンタ
cell_counter = 0

for item in data:

    # lastの写真を張る動作
    infra_pass = R'C:\work\django\myproject\myvenv\Infraproject\infra\static'
    for image_sub_path in item['this_time_picture']:
        image_path = os.path.join(infra_pass, image_sub_path)
        print(image_path)
        if os.path.exists(image_path):
            img = Image(image_path) # 画像の読み込み
            print(img)
            img.width, img.height = max_width, max_height # 画像サイズの設定    
            cell_pos = picture_cell_positions[cell_counter // 3][cell_counter % 3] # 所定のセル位置       
            ws.add_image(img, cell_pos) # ワークシートに画像を追加 
            cell_counter += 1 # カウンタを一つ進める 
        

new_file_path = 'C:/Users/dobokuka4/Desktop/sample.xlsx'

# 新しいファイル名で保存
wb.save(new_file_path)
