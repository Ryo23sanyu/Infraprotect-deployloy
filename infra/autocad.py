# @title デフォルトのタイトル テキスト
# C:\work\django\myproject\myvenv\Scripts\python.exe
import ezdxf
from ezdxf.entities.mtext import MText
import pandas as pd

dxf = ezdxf.readfile(R'C:\work\django\myproject\myvenv\Infraproject\uploads\12_細握橋.dxf') # ファイルにアップロードしたdxfファイル名

cad_read = []
for entity in dxf.entities:
    if type(entity) is MText: # or type(entity) is Text: MTextとTextが文字列を表す(https://ymt-lab.com/post/2021/ezdxf-read-dxf-file/)
        cad =  entity.plain_text() # plain_text(読める文字)に変換
        cad_data = cad.split("\n") if len(cad) > 0 else [] # .split():\nの箇所で配列に分配
        if len(cad_data) > 0:
            cad_read.append(cad_data)

dix = pd.DataFrame( cad_read, columns=['部材名', '損傷名1', '損傷名2', '損傷名3', '損傷名4'] ) # 列のタイトルの設定
dix.insert(2, '余白', "") # 列の追加

dix.to_csv('output.csv', index=False)  # dixをCSVファイルとして保存
df = pd.read_csv('output.csv')  # 保存したCSVファイルを読み込み

def write_html(df, output):
    scripts = """
    <link href="https://cdn.datatables.net/v/dt/jq-3.6.0/dt-1.13.4/datatables.min.css" rel="stylesheet"/>
    <script src="https://cdn.datatables.net/v/dt/jq-3.6.0/dt-1.13.4/datatables.min.js"></script>
    <script>$(document).ready(function() {$('.my-table').DataTable({});})</script>

    <script>
    $(document).ready(function() {
        $.extend( $.fn.dataTable.defaults, { 
            language: {
                url: "https://cdn.datatables.net/plug-ins/1.13.7/i18n/ja.json"
            } 
        });
    
        $('.my-table').DataTable({
            select: true, #行の選択
            displayLength: 25, #表示する行数
            buttons: ['copy'], #コピーボタンの追加
            fixedHeader: true, #ヘッダーの固定
            dom: 'iQrtBlp', #i(表の情報を表示),Q(検索ボックス),r(表示件数の選択ボックス),t(テーブル要素),B(ボタン要素),lp(ページング要素)
        });
    });
    </script>
    """

    html = df.to_html(classes='my-table')
    html = scripts + html
    with open(output, mode='w', encoding="utf-8") as file:# "w":上書き
    # with open(output, mode='a', encoding="utf-8") as file:# "a":末尾に追記
        file.write(html)

write_html(df, 'future.html')