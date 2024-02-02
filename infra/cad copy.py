# @title デフォルトのタイトル テキスト
# C:\work\django\myproject\myvenv\Scripts\python.exe
import ezdxf
from ezdxf.entities.mtext import MText
import pandas as pd

dxf = ezdxf.readfile(R'C:\work\django\myproject\myvenv\Infraproject\uploads\5_大久保歩道橋.dxf') # ファイルにアップロードしたdxfファイル名

cad_read = []
for entity in dxf.entities:
    if type(entity) is MText: # or type(entity) is Text: MTextとTextが文字列を表す(https://ymt-lab.com/post/2021/ezdxf-read-dxf-file/)
        cad =  entity.plain_text() # plain_text(読める文字)に変換
        cad_data = cad.split("\n") if len(cad) > 0 else [] # .split():\nの箇所で改行
        if len(cad_data) > 0:
            cad_read.append(cad_data)

dix = pd.DataFrame( cad_read )

dix.to_csv('output.csv', index=False)  # dixをCSVファイルとして保存
df = pd.read_csv('output.csv').iloc[:100, :]  # 保存したCSVファイルを読み込み

def write_html(df, output):
    scripts = """
    <link href="https://cdn.datatables.net/v/dt/jq-3.6.0/dt-1.13.4/datatables.min.css" rel="stylesheet"/>
    <script src="https://cdn.datatables.net/v/dt/jq-3.6.0/dt-1.13.4/datatables.min.js"></script>
    <script>$(document).ready(function() {$('.my-table').DataTable({});})</script>
    """

    html = df.to_html(classes='my-table')
    html = scripts + html
    with open(output, mode='a', encoding="utf-8") as file:# "a":末尾に追記
        file.write(html)

write_html(df, 'future.html')