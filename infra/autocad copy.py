# @title デフォルトのタイトル テキスト
# C:\work\django\myproject\myvenv\Scripts\python.exe
import ezdxf
from ezdxf.entities.mtext import MText
import pandas as pd

filename = R'C:\work\django\myproject\myvenv\Infraproject\uploads\12_細握橋.dxf'

# DXFファイル内のすべてのエンティティを取得
def extract_entities(filename):
    doc = ezdxf.readfile(filename)
    modelspace = doc.modelspace() # AutoCADのドキュメントのモデルスペースを取得
    entities = [] # 空のリストを作成して格納
    for entity in modelspace: # modelspaceの中の各要素を順番に取り出すためのループ処理
        entities.append(entity) #entitiesリストにループで取り出したentityを追加
    return entities # entitiesリストを返す

# 取得したエンティティの中から特定のポリラインを見つける
def find_boundaries(entities):
    boundaries = []
    for entity in entities:
        if entity.dxftype() == 'Defpoints':
            # ここでは特定の条件(例: レイヤー名が'BOUNDARY'など)でポリラインを判別することができます
            # 特定のポリラインを見つけた場合、そのポリラインの頂点情報を取得します
            vertices = entity.get_points()
            boundaries.append(vertices)
    return boundaries

# 特定のポリラインの内部にあるエンティティを抽出
def extract_inner_entities(entities, boundaries):
    inner_entities = []
    for entity in entities:
        for boundary in boundaries:
            if is_inside_boundary(entity, boundary):
                inner_entities.append(entity)
                break
    return inner_entities

# 特定のポリラインの内部にあるかどうかを判定
def is_inside_boundary(entity, boundary):
    x, y, _ = entity.dxf.location
    num_vertices = len(boundary)
    inside = False
    j = num_vertices - 1
    for i in range(num_vertices):
        if ((boundary[i][1] > y) != (boundary[j][1] > y)) and \
                (x < (boundary[j][0] - boundary[i][0]) * (y - boundary[i][1]) /
                (boundary[j][1] - boundary[i][1]) + boundary[i][0]):
            inside = not inside
        j = i
    return inside

entities = extract_entities(filename)
boundaries = find_boundaries(entities)
inner_entities = extract_inner_entities(entities, boundaries)

for entity in entities:
    if type(entity) is ezdxf.entities.MText: # or type(entity) is Text: MTextとTextが文字列を表す(https://ymt-lab.com/post/2021/ezdxf-read-dxf-file/)
        cad =  entity.plain_text() # plain_text(読める文字)に変換
        cad_data = cad.split("\n") if len(cad) > 0 else [] # .split():\nの箇所で改行
        if len(cad_data) > 0:
            inner_entities.append(cad_data)
            
dix = pd.DataFrame( inner_entities, columns=['部材名', '損傷名1', '損傷名2', '損傷名3', '損傷名4'] ) # 列のタイトルの設定
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
        
write_html(df, 'aaa.html')