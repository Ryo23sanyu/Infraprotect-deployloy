import openpyxl
from openpyxl.worksheet.header_footer import HeaderFooter

def add_header_and_footer(file_path, header_text, footer_text):
    # Workbookを読み込み
    workbook = openpyxl.load_workbook(file_path)

    # 各シートにヘッダーとフッターを挿入
    for sheet_name in workbook.sheetnames:
        sheet = workbook[sheet_name]

        # ヘッダーとフッターの設定
        sheet.header_footer = HeaderFooter(text_left=header_text, text_right=footer_text)

    # ファイル保存
    workbook.save(file_path)

# Excelファイルのパスと挿入するヘッダー、フッターのテキストを指定
file_path = 'output.xlsx'
header_text = 'Your Header Text'
footer_text = 'Your Footer Text'

# ヘッダーとフッターを挿入
add_header_and_footer(file_path, header_text, footer_text)
