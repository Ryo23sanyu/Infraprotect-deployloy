import datetime
from io import BytesIO
import os
import openpyxl

# Django管理サイトからデータを取得
records = FullReportData.objects.all()
# 元のファイルのパス（例: `10_only.xlsm`）
original_file_path = '10_only.xlsm'
# エクセルファイルを読み込む
wb = openpyxl.load_workbook(original_file_path, keep_vba=True)


# << その10入力欄 >>(+14)
# I9 ,AI9 ,BI9 ,23,37 # 写真番号           /None
# R9 ,AR9 ,BR9 ,23,37 # 径間番号           /span_number
# I10,AI10,BI10,24,38 # 部材名(主桁)       /parts_name
# I11,AI11,BI11,25,39 # 損傷の種類(ひびわれ)/damage_name
# R10,AR10,BR10,24,38 # 要素番号(0101)     /parts_name
# R11,AR11,BR11,25,39 # 損傷程度(e)        /damage_name
# E13,AE13,BE13,27,41 # 写真               /this_time_picture
# T15,AT15,BT15,29,43 # 前回損傷程度       /None
# T17,AT17,BT17,31,45 # メモ               /textarea_content

# 現在の日時を取得してファイル名に追加
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
# 新しいファイル名の生成
new_filename = f"{timestamp}_Macro_{original_file_path}"
# デスクトップのパス
# desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
# 保存するファイルのフルパス
# save_path = os.path.join(desktop_path, new_filename)
""""""
#メモリ空間内に保存
virtual = BytesIO()
wb.save(virtual)