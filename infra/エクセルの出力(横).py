# from .models import YourModel
# data = YourModel.objects.all()

from openpyxl import load_workbook
from itertools import cycle
# 既存のExcelファイルを開く
wb = load_workbook('sample.xlsx')

# シートを選択
sheet = wb['その３']

# Djangoから取得したデータをリストに格納（例示）
# data_list = [obj.some_field for obj in data]
data_list = ['A', 'B', 'C', 'D', 'E', 'F']

# 出力を開始する行番号を指定
start_row = 1

# 指定された列でデータを横並びに出力するための列のリスト
columns = cycle(['B', 'E', 'H'])  # 循環するリスト

# データをExcelに出力
for i, value in enumerate(data_list):
    column = next(columns)  # 次の列を取得

    # データを書き込むセルを指定
    cell = f'{column}{start_row}'
    sheet[cell] = value

    # H列にデータを書き込んだ後、次の行に移動
    if column == 'H':
        start_row += 1

# 別名で保存するため、新しいファイル名を指定
new_file_path = r'C:\Users\dobokuka4\Desktop\tameshi.xlsx'
# macの場合(new_file_path = '/Users/YourUsername/Desktop/example.xlsx')

# 新しいファイル名で保存
wb.save(new_file_path)