import os
import openpyxl
from openpyxl.drawing.image import Image
from PIL import Image as PILImage
from io import BytesIO

def extract_images_and_find_photo_number(excel_file, sheet_name, output_folder):
    # 保存先フォルダが存在しない場合は作成
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Excelファイルを読み込む
    wb = openpyxl.load_workbook(excel_file, data_only=True)
    sheet = wb[sheet_name]
    
    # 「写真番号」と書かれているセルを探す
    photo_number_positions = []
    for row in sheet.iter_rows(values_only=False):
        for cell in row:
            if cell.value == "写真番号":
                photo_number_positions.append((cell.row, cell.column))
                print(f"写真番号 found at Row: {cell.row}, Column: {cell.column}")
                
    
    # シート内の画像を収集
    images = []
    for img in sheet._images:
        images.append((img.anchor._from.row, img.anchor._from.col, img))
    
    # 行方向に並べ替え
    images.sort(key=lambda x: (x[0], x[1]))
    
    # 画像位置の表示
    for row, col, img in images:        
        print(f"Image found at Row: {row}, Column: {col}")

    return photo_number_positions

# 使い方
excel_file = R'C:\work\django\myproject\program\Infraproject\uploads\たぬき橋.xlsx'
sheet_name = 'その１０'  # 抽出したいシート名を指定
output_folder = '前回写真'  # 保存先フォルダを指定

photo_number_positions = extract_images_and_find_photo_number(excel_file, sheet_name, output_folder)