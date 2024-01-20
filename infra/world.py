from lib2to3.pgen2.pgen import DFAState
import pandas as pd
import os

# フォルダ内の画像ファイルのパスを取得
image_folder_path = R'C:\\Users\\dobokuka4\\Desktop\\new'  # 画像が格納されているフォルダのパスを指定
image_files = [f for f in os.listdir(image_folder_path) if f.endswith(('.jpg', '.png'))]# pdfを追加する場合は末尾に.pdfを追加

# 画像URLが格納された列を用意
DFAState['photo_url'] = [os.path.join(image_folder_path, file) for file in image_files]

# 1ページあたりの行数
rows_per_page = 10

# ページごとにデータを分割
num_pages = len(DFAState) // rows_per_page + 1
for page in range(num_pages):
    # ページごとのデータフレームを作成
    start_idx = page * rows_per_page
    end_idx = (page + 1) * rows_per_page
    page_df = DFAState.iloc[start_idx:end_idx]

    # 写真URLをHTMLタグに変換
    page_df['photo_html'] = page_df['photo_url'].apply(lambda x: f'<img src="{x}" style="max-width: 100px; max-height: 100px;">')

    # 表示用のHTMLに変換
    page_html = page_df.to_html(classes='my-table', escape=False, render_links=True)

    # スタイルやスクリプトを追加
    scripts = """
    <link href="https://cdn.datatables.net/v/dt/jq-3.6.0/dt-1.13.4/datatables.min.css" rel="stylesheet"/>
    <script src="https://cdn.datatables.net/v/dt/jq-3.6.0/dt-1.13.4/datatables.min.js"></script>
    <script>$(document).ready(function() {$('.my-table').DataTable({});})</script>
    """

    page_html = scripts + page_html

    # ページごとにファイルに書き込み
    with open(f'fuga_page_{page + 1}.html', mode='w', encoding='utf-8') as f:
        f.write(page_html)
