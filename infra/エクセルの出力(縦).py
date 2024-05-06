from .models import YourModel
data = YourModel.objects.all()

from openpyxl import load_workbook
# 元のファイルをロード
wb = load_workbook('base.xlsx')

# 第3シートを選択（シートの名前によって選択します）
sheet = wb['その３']

# Djangoから取得したデータをリストに格納（例示です）
data_list = [obj.some_field for obj in data]

# <<G1, AA1, AU1 セルにデータを出力し、ループでG18, AA18, AU18...にデータを格納>>
# ベースとなるセルの指定
cells = ['G1', 'AA1', 'AU1']
#
for i, value in enumerate(data_list):
    # cellsリストの中の各cellについて、ループを実行
    for cell in cells:
        # 行番号の開始位置を見つけます
        for i in range(len(cell)):
            if cell[i].isdigit():
                break

        # 列と行に分割
        col, row = cell[:i], int(cell[i:])
            
        # インデックスiに応じて行を18ずつ増やす(i=0:1,i=1:18,i=2:36,...)
        row += i * 17
        # colとrowを合わせて新しいセル番号を作成
        new_cell = f'{col}{row}'
        # セル番地(new_cell)を使用して、そのセルにvalue(data_listから取得した現在の値)を設定
        # sheetは前の行で設定したエクセルのシートオブジェクト
        sheet[new_cell] = value

# 別名で保存するため、新しいファイル名を指定
new_file_path = 'C:/Users/dobokuka4/Desktop/tameshi.xlsx'
# macの場合(new_file_path = '/Users/YourUsername/Desktop/example.xlsx')

# 新しいファイル名で保存
wb.save(new_file_path)