import re
import ezdxf
from ezdxf.entities.mtext import MText
import pandas as pd

def extract_text(filename):
    doc = ezdxf.readfile(filename)
    msp = doc.modelspace()
    
    extracted_text = []
    for entity in msp:
        if entity.dxftype() == 'MTEXT':
            # MTextのテキストを抽出する
            text = entity.plain_text()
            cad_data = text.split("\n") if len(text) > 0 else [] # .split():\nの箇所で配列に分配
            if len(cad_data) > 0 and not text.startswith("※") and not any(keyword in text for keyword in ["×", ".", "損傷図"]):
             # 改行を含むかどうかをチェックする(and "\n" in cad):# 特定の文字列で始まるかどうかをチェックする: # 特定の文字を含むかどうかをチェックする
                extracted_text.append(cad_data)
            
            # MTextの下、もしくは右に特定のプロパティ(Defpoints)で描かれた文字を探す
            for neighbor in msp.query('TEXT[layer=="Defpoints"]'):
                # MTextの挿入位置と特定のプロパティで描かれた文字の位置を比較する
                if entity_extension(entity, neighbor):
                    # 特定のプロパティ(Defpoints)で描かれた文字のテキストを抽出する
                    neighbor_text = neighbor.plain_text()
                    extracted_text.append(neighbor_text)
    
    return extracted_text

def entity_extension(mtext, neighbor):
    # MTextの挿入点
    mtext_insertion = mtext.dxf.insert
    
    # 特定のプロパティ(Defpoints)で描かれた文字の挿入点
    neighbor_insertion = neighbor.dxf.insert
    
    # MTextの下、もしくは右に特定のプロパティで描かれた文字が存在するかどうかを判定する
    if (
        neighbor_insertion[0] >= mtext_insertion[0]
        and neighbor_insertion[0] <= mtext_insertion[0]
    ):
        if (
            neighbor_insertion[1] >= mtext_insertion[1]
            and neighbor_insertion[1] <= mtext_insertion[1]
        ):
            return True
    
    return False



# AutoCADファイル名を指定してテキストを抽出する
filename = R'C:\work\django\myproject\myvenv\Infraproject\uploads\121_損傷橋.dxf'
extracted_text = extract_text(filename)

for index, data in enumerate(extracted_text):
    # 最終項目-1まで評価
    if index < (len(extracted_text) -1):
        # 次の位置の要素を取得
        next_data = extracted_text[index + 1]
        # 特定の条件(以下例だと、１要素目が文字s1,s2,s3から始まる）に合致するかチェック
        if ("月" in next_data[0] and "日" in next_data[0]) or ("/" in next_data[0]) and (re.search(r"[A-Z]", next_data[0], re.IGNORECASE) and re.search(r"[0-9]", next_data[0])):
            # 合致する場合現在の位置に次の要素を併合 and "\n" in cad
            data.extend(next_data)
            # 次の位置の要素を削除
            extracted_text.remove(next_data)
print(extracted_text)

# 先頭の要素を抽出
first_item = [sub_list[0] for sub_list in extracted_text]
# それ以外の要素を抽出
second_items = [sub_list[1:-2] for sub_list in extracted_text]
# 最後から2番目の要素を抽出
third_items = [sub_list[-2] for sub_list in extracted_text if len(sub_list) >= 2]
# 最後の要素を抽出
last_item = [sub_list[-1] for sub_list in extracted_text]

table = []  # 空のリストを作成

# ループで各要素を辞書型に変換し、空のリストに追加
for i in range(len(first_item)):
    item = {'first': first_item[i], 'second': second_items[i], 'third': third_items[i], 'last': last_item[i]}
    table.append(item)

# 結果を表示
print(table)