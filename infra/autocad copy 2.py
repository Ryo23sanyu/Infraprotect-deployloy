# @title デフォルトのタイトル テキスト
# C:\work\django\myproject\myvenv\Scripts\python.exe
import ast
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

processed_data = str(cad_read)
processed_data_with_quotes = '"' + processed_data + '"'

data = processed_data_with_quotes

list_of_lists = data.replace("[[", "").replace("]]", "").split("], [")

data_list = ast.literal_eval(data)

data_list = append(item[0]) 



# 空のリストを作成
result = []

# リスト内の要素を取り出し、辞書に変換し、resultに追加
for sublist in list_of_lists:
    dictionary = {}  # 辞書を初期化
    items = sublist.split(", ")  # 要素をカンマごとに分割
    dictionary['name'] = items[0].strip()  # 1つ目の要素がname
    dictionary['age'] = items[1:-1].strip()  # 2つ目の要素がage
    dictionary['gender'] = items[-1].strip()  # 3つ目の要素がgender
    result.append(dictionary)

print(result)