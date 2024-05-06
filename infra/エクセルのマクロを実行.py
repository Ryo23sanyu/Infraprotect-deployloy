import win32com.client as win32

# Excelファイルを開く（ここにファイルパスを指定）
excel_path = r'C:\work\django\myproject\program\Infraproject\base.xlsm'

# Excelアプリケーションを起動
excel_app = win32.Dispatch("Excel.Application")
excel_app.Visible = False  # Excelアプリケーションを可視状態で起動するためTrueに設定

# ワークブックを開く
wb = excel_app.Workbooks.Open(excel_path)

# シートを指定
sheet = wb.Sheets('その１')
# AR10セルに "python" を入力
sheet.Range('BC5').Value = "python"

# シートを指定
sheet = wb.Sheets('その１０')
# AR10セルに "python" を入力
sheet.Range('R10').Value = "8"

# マクロを実行（ここでは'MacroName'という名前のマクロを実行する）
excel_app.Run('千葉県様式作成')

# 別名で保存するため、新しいファイル名を指定
new_file_path = r'C:\Users\dobokuka4\Desktop\テスト.xlsx'
# macの場合(new_file_path = '/Users/YourUsername/Desktop/example.xlsx')

# 新しいファイル名で保存
wb.SaveAs(new_file_path)  # SaveからSaveAsに変更

wb.Close()

excel_app.Quit()  # Excelアプリケーションを閉じる