import ezdxf
import openpyxl

def extract_text_from_dxf(file_path):
    text_data = []
    doc = ezdxf.readfile(file_path)
    msp = doc.modelspace()

    # DXFファイルからテキストデータを抽出
    for text in msp.query('MTEXT'):
        text_data.append(text.dxf.text)

    return text_data

def display_data_with_keywords(text_data, excel_file):
    # Excelファイルを開く
    wb = openpyxl.load_workbook(excel_file)
    sheet = wb['リスト']

    # キーワードを取得
    keywords = []
    for row in sheet.iter_rows(min_row=5, max_row=72, min_col=24, max_col=24, values_only=True):
        for cell in row:
            if cell:
                keywords.append(cell)

    # 各キーワードに対応するデータを保持する辞書を初期化
    data_for_keywords = {keyword: [] for keyword in keywords}

    # DXFファイルから取得したテキストデータを元に各キーワードに対応するデータを抽出
    for keyword in keywords:
        for text in text_data:
            if str(keyword) in text:
                data_for_keywords[keyword].append(text)

    # 各キーワードに対応するデータを表示
    for keyword, data in data_for_keywords.items():
        print(f"キーワード '{keyword}' を含むデータ:")
        for item in data:
            print(item)
        print()

# DXFファイルからテキストデータを抽出
dxf_file_path = r'C:\work\django\myproject\myvenv\Infraproject\uploads\12_損傷橋.dxf'
text_data = extract_text_from_dxf(dxf_file_path)

# Excelファイルからデータを読み込んで、キーワードごとにデータを表示
excel_file_path = r'C:\Users\dobokuka4\Desktop\macro.xlsx'
display_data_with_keywords(text_data, excel_file_path)
