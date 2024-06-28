import datetime
from itertools import zip_longest
import re
from django.conf import settings
import openpyxl
from openpyxl.drawing.image import Image
# プログラム1｜win32comライブラリの設定
import win32com.client
import os


# 指定したエクセルファイルを開く
# プログラム2｜Excelアプリケーションを起動
Excel = win32com.client.Dispatch('Excel.Application')
Excel.Visible = False # Trueにするとエクセル画面が表示
Excel.DisplayAlerts = False # Trueにすると警告ダイアログや確認ダイアログを表示

# プログラム3｜エクセルを開く
filename = '10_only.xlsm'
fullpath = os.path.join(os.getcwd(),filename)
wb = Excel.Workbooks.Open(Filename=fullpath)
ws = wb.Worksheets('その１０')  # シート名を指定

# CF3セルに値を入力
# TODO：径間番号を右辺にあてはめる
ws.Range("CF3").Value = "2"

# シート複製マクロを実行
macro_name = 'シート複製'
Excel.Application.Run(f"'{filename}'!{macro_name}")

# 新しいシートに移動
# TODO：それぞれの径間番号を「その１０-」の後ろに貼付け
ws = wb.Worksheets('その１０-1') # シート名を指定

sorted_items = [
    {'parts_name': [['排水管 Dp0101']], 'damage_name': [['①腐食(大大)-e', '⑤防食機能の劣化(分類1)-e']], 
     'join': [{'parts_name': ['排水管 Dp0101'], 'damage_name': ['①腐食(大大)-e', '⑤防食機能の劣化(分類1)-e']}], 
     'picture_number': '写真番号-31', 'this_time_picture': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070617.JPG'], 
     'last_time_picture': None, 
     'textarea_content': '排水管に板厚減少を伴う拡がりのある腐食,点錆が見られる。\n【関連損傷】\n排水管 Dp0101:⑤防食機能の劣化(分類1)-e', 
     'damage_coordinate': ['538482.3557216563', '229268.8593029478'], 'picture_coordinate': ['538810.3087944178', '228910.3502713814']}
]
# infra/img\\9月7日\u3000佐藤\u3000地上\\P9070617.JPG
# C:\work\django\myproject\program\Infraproject\infra\static\infra\img\9月7日　佐藤　地上\P9070617.JPG
# C:\work\django\myproject\program\Infraproject\infra\static\infra\img\9月7日　佐藤　地上\P9070617.JPG
# lastがNoneでないデータを残す
filtered_data = [item for item in sorted_items if item['this_time_picture'] is not None]

# this_time_pictureの要素が複数ある場合、分割する
output_data = []
for entry in filtered_data:
    for picture in entry['this_time_picture']:
        new_entry = entry.copy()
        new_entry['this_time_picture'] = [picture]
        output_data.append(new_entry)
        
# 行の開始地点と増加するステップを定義
partsname_and_number_row = 10 # 部材名・要素番号
damagename_and_lank_row = 11 # 損傷の種類・損傷程度
picture_start_row = 13 # 損傷写真
lasttime_lank_row = 15 # 前回損傷程度
damage_memo_row = 17 # 損傷メモ
step = 14
num_positions = len(output_data) * 3  # データ数に3列分を掛けています

# 関連する列を定義
picture_columns = ["E", "AE", "BE"]
left_columns = ["I", "AI", "BI"]
right_columns = ["R", "AR", "BR"]
bottom_columns = ["T", "AT", "BT"]

# セル位置のリストを生成 ↓
partsname_cell_positions = [] # 部材名
number_cell_positions = [] # 要素番号
damagename_cell_positions = [] # 損傷の種類
lank_cell_positions = [] # 損損傷程度
picture_cell_positions = [] # 損傷写真
lasttime_lank_cell_positions = [] # 前回損傷程度
damage_memo_cell_positions = [] # 損傷メモ

for i in range(num_positions // len(picture_columns)):
    partsname_cell_positions.append([f"{col}{partsname_and_number_row + i * step}" for col in left_columns])
    number_cell_positions.append([f"{col}{partsname_and_number_row + i * step}" for col in right_columns])
    damagename_cell_positions.append([f"{col}{damagename_and_lank_row + i * step}" for col in left_columns])
    lank_cell_positions.append([f"{col}{damagename_and_lank_row + i * step}" for col in right_columns])
    picture_cell_positions.append([f"{col}{picture_start_row + i * step}" for col in picture_columns])
    lasttime_lank_cell_positions.append([f"{col}{lasttime_lank_row + i * step}" for col in bottom_columns])
    damage_memo_cell_positions.append([f"{col}{damage_memo_row + i * step}" for col in bottom_columns])
    
join_partsname_cell_positions = [item for sublist in partsname_cell_positions for item in sublist]
join_number_cell_positions = [item for sublist in number_cell_positions for item in sublist]
join_damagename_cell_positions = [item for sublist in damagename_cell_positions for item in sublist]
join_lank_cell_positions = [item for sublist in lank_cell_positions for item in sublist]
join_picture_cell_positions = [item for sublist in picture_cell_positions for item in sublist]
join_lasttime_lank_cell_positions = [item for sublist in lasttime_lank_cell_positions for item in sublist]
join_damage_memo_cell_positions = [item for sublist in damage_memo_cell_positions for item in sublist]
# セル位置のリストを生成 ↑

number_change = {
'①': '腐食',
'②': '亀裂',
'③': 'ゆるみ・脱落',
'④': '破断',
'⑤': '防食機能の劣化',
'⑥': 'ひびわれ',
'⑦': '剥離・鉄筋露出',
'⑧': '漏水・遊離石灰',
'⑨': '抜け落ち',
'⑩': '補修・補強材の損傷',
'⑪': '床版ひびわれ',
'⑫': 'うき',
'⑬': '遊間の異常',
'⑭': '路面の凹凸',
'⑮': '舗装の異常',
'⑯': '支承部の機能障害',
'⑰': 'その他',
'⑱': '定着部の異常',
'⑲': '変色・劣化',
'⑳': '漏水・滞水',
'㉑': '異常な音・振動',
'㉒': '異常なたわみ',
'㉓': '変形・欠損',
'㉔': '土砂詰まり',
'㉕': '沈下・移動・傾斜',
'㉖': '洗掘',
}

# 最大の写真サイズ（幅、高さ）
max_width, max_height = 180, 150 # 4:3

# 位置を追跡するカウンタ
cell_counter = 0

def convert_backslash_to_slash(path):
    return path.replace("/", "\\")

for item in output_data:
    # 3列目(インデックスが2)でpictureキーに写真が設定されている場合
    if cell_counter % 2 == 0 and item['last_time_picture'] is not None:
        # 3列目を空白にするため、インデックスを1つ追加
        cell_counter += 1
    # pictureキーに写真が設定されていても、3列目でなければOK
    else:
        pass
    
    if cell_counter % 6 == 5 and cell_counter > 10:
        # プログラム4｜マクロ実行
        macro_name = 'ページ複製その10'
        Excel.Application.Run(f"'{filename}'!{macro_name}")

    # 現在の画像を貼り付ける動作
    for image_path in item['this_time_picture']:
        full = "C:\work\django\myproject\program\Infraproject\infra\static"
        sub_image_path_full = os.path.join(full, image_path) # フルパスを取得
        image_path_full = convert_backslash_to_slash(sub_image_path_full)
        print(image_path_full)
        if os.path.exists(image_path_full):
            print('true')
            print(image_path_full)
            cell_pos = picture_cell_positions[cell_counter // len(picture_columns)][cell_counter % len(picture_columns)]  # 所定のセル位置
            left = ws.Range(cell_pos).Left  # セルの左辺の位置を取得
            top = ws.Range(cell_pos).Top  # セルの上辺の位置を取得
            ws.Shapes.AddPicture(image_path_full, 0, 1, left, top, max_width, max_height)  # 画像を追加
            cell_counter += 1  # カウンタを進める
        else:
            print('false')

    # 過去の画像を貼り付ける動作
    if item['last_time_picture'] and os.path.exists(item['last_time_picture']):
        img_path = os.path.abspath(item['last_time_picture'])
        print(img_path)
        cell_pos = picture_cell_positions[cell_counter // len(picture_columns)][cell_counter % len(picture_columns)]
        left = ws.Range(cell_pos).Left  # セルの左辺の位置を取得
        top = ws.Range(cell_pos).Top    # セルの上辺の位置を取得
        ws.Shapes.AddPicture(img_path, 0, 1, left, top, max_width, max_height)
        cell_counter += 1  # カウンタを進める
        
# データの入力
data_index = 0

def extract_cell_value(cell_str):
    match = re.match(r"([A-Z]+)([0-9]+)", cell_str)
    if match:
        col_str, row_str = match.groups()
        row = int(row_str)
        col = sum([(ord(char) - 64) * (26 ** idx) for idx, char in enumerate(reversed(col_str))])
        return (row, col)
    return None

for item, part_pos, number_pos, name_pos, lank_pos, memo_pos, picture_pos in zip_longest(output_data, join_partsname_cell_positions, join_number_cell_positions, join_damagename_cell_positions, join_lank_cell_positions, join_damage_memo_cell_positions, join_picture_cell_positions, fillvalue=None):
    
    if (data_index == 2 or data_index % 2 == 3) and item['last_time_picture'] is not None:
        data_index += 1

    part_cell = extract_cell_value(join_partsname_cell_positions[data_index])
    number_cell = extract_cell_value(join_number_cell_positions[data_index])
    name_cell = extract_cell_value(join_damagename_cell_positions[data_index])
    post_lank_cell = extract_cell_value(join_lank_cell_positions[data_index])
    pre_lank_cell = extract_cell_value(join_lasttime_lank_cell_positions[data_index])
    memo_cell = extract_cell_value(join_damage_memo_cell_positions[data_index])
    
# メモに入れるための固定コード　↓
    # firstキーの内容を所定の書式に変更
    try:
        first_data = item['parts_name'][0][0]
        split_space = first_data.split(" ")
        first_part_data = split_space[0]

        match = re.search(r'\d+', split_space[1])
        first_number_data = match.group() if match else ''

        if part_cell:
            ws.Cells(part_cell[0], part_cell[1]).Value = first_part_data
        if number_cell:
            ws.Cells(number_cell[0], number_cell[1]).Value = first_number_data

        second_data = item['damage_name'][0][0]
        second_damage_name = second_data[0]
        second_name_data = number_change.get(second_damage_name, second_damage_name)
        second_lank_data = second_data[-1]

        if name_cell:
            ws.Cells(name_cell[0], name_cell[1]).Value = second_name_data
        if post_lank_cell:
            ws.Cells(post_lank_cell[0], post_lank_cell[1]).Value = second_lank_data

        memo_data = item['textarea_content']
        if memo_cell:
            ws.Cells(memo_cell[0], memo_cell[1]).Value = memo_data

        if item['last_time_picture'] is not None:
            data_index += 2
        else:
            data_index += 1
            
    except (TypeError, KeyError):
        if part_cell:
            ws.Cells(part_cell[0], part_cell[1]).Value = ""
        if number_cell:
            ws.Cells(number_cell[0], number_cell[1]).Value = ""
        if name_cell:
            ws.Cells(name_cell[0], name_cell[1]).Value = ""
        if post_lank_cell:
            ws.Cells(post_lank_cell[0], post_lank_cell[1]).Value = ""
        if memo_cell:
            ws.Cells(memo_cell[0], memo_cell[1]).Value = ""
        
# メモに入れるための固定コード　↑

# プログラム5｜エクセルを保存して閉じる
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
newfilename = timestamp + 'Macro_' + filename
if os.name == 'nt':  # Windowsの場合
    desktop_path = r'C:\Users\dobokuka4\Desktop'
elif os.name == 'posix':  # Macの場合 (および他のUNIX系)
    desktop_path = r'\Users\dobokuka4\Desktop'
else:
    raise EnvironmentError('Unsupported platform')
newfullpath = os.path.join(desktop_path,newfilename)
wb.SaveAs(newfullpath)
wb.Close()

# プログラム6｜Excelアプリケーションを閉じる
Excel.DisplayAlerts = True
Excel.Application.Quit()