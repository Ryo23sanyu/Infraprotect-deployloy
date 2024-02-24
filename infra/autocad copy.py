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
        if entity.dxftype() == '枠':
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

print(inner_entities)