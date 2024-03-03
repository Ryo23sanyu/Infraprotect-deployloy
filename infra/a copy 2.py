import re
import ezdxf
from ezdxf.entities.mtext import MText
import pandas as pd

def extract_text(filename):
    doc = ezdxf.readfile(filename)
    msp = doc.modelspace()
    
    extracted_text = []
    for mtext in msp:
        if mtext.dxftype() == 'MTEXT':
            # MTextのテキストを抽出する
            text = mtext.plain_text()
            cad_data = text.split("\n") if len(text) > 0 else [] # .split():\nの箇所で配列に分配
            if len(cad_data) > 0 and not text.startswith("※") and not any(keyword in text for keyword in ["×", ".", "損傷図"]):
             # 改行を含むかどうかをチェックする(and "\n" in cad):# 特定の文字列で始まるかどうかをチェックする: # 特定の文字を含むかどうかをチェックする
            
            # MTextの下、もしくは右に特定のプロパティ(Defpoints)で描かれた文字を探す
                for neighbor in msp.query('TEXT[layer=="Defpoints"]'):
                # MTextの挿入位置と特定のプロパティで描かれた文字の位置を比較する
                    if entity_extension(mtext, neighbor):
                    # 特定のプロパティ(Defpoints)で描かれた文字のテキストを抽出する
                        neighbor_text = neighbor.plain_text()
                        extracted_text.append([mtext.text, neighbor.text])
            
def entity_extension(mtext, neighbor):
    # MTextの挿入点
    mtext_insertion = mtext.dxf.insert
    # 特定のプロパティ(Defpoints)で描かれた文字の挿入点
    neighbor_insertion = neighbor.dxf.insert
    #テキストの行数を求める
    text = mtext.plain_text()
    text_lines = text.split("\n") if len(text) > 0 else []
    # 改行で区切ったリスト数→行数
    text_lines_count = len(text_lines)
    
    # Defpointsを範囲内とするX座標範囲
    x_start = mtext_insertion[0]  # X開始位置
    x_end  = mtext_insertion[0] + mtext.dxf.width # X終了位置= 開始位置＋幅
    y_start = mtext_insertion[1] + mtext.dxf.char_height * text_lines_count # Y開始位置
    y_end  = mtext_insertion[1] - mtext.dxf.char_height * (text_lines_count + 1) # 文字の高さ×(行数+1)
                
    if (neighbor_insertion[0] >= x_start and neighbor_insertion[0] <= x_end):
        if (neighbor_insertion[1] >= y_end and neighbor_insertion[1] <= y_start):
            return True
    return False

# AutoCADファイル名を指定してテキストを抽出する
filename = R'C:\work\django\myproject\myvenv\Infraproject\uploads\121_損傷橋.dxf'
extracted_text = extract_text(filename)

print(extracted_text)

# for index, data in enumerate(extracted_text):
#     # 最終項目-1まで評価
#     if index < (len(extracted_text) -1):
#         # 次の位置の要素を取得
#         next_data = extracted_text[index + 1]
#         # 特定の条件(以下例だと、１要素目が文字s1,s2,s3から始まる）に合致するかチェック
#         if ("月" in next_data[0] and "日" in next_data[0]) or ("/" in next_data[0]) and (re.search(r"[A-Z]", next_data[0], re.IGNORECASE) and re.search(r"[0-9]", next_data[0])):
#             # 合致する場合現在の位置に次の要素を併合 and "\n" in cad
#             data.extend(next_data)
#             # 次の位置の要素を削除
#             extracted_text.remove(next_data)
# print(extracted_text)

# # 先頭の要素を抽出
# first_item = [sub_list[0] for sub_list in extracted_text]

# # リストの各要素から記号を削除する
# def remove_symbols(other_items):
#     symbols = ['!', '[', ']', "'"]

#     processed_other_items = []
#     for item in other_items:
#         processed_item = ''.join(c for c in item if c not in symbols)
#         processed_other_items.append(processed_item)
   
#     return processed_other_items
# # それ以外の要素を抽出
# other_items = [sub_list[1:-2] for sub_list in extracted_text]
# second_items = remove_symbols(other_items)

# # 最後から2番目の要素を抽出
# third_items = [sub_list[-2] for sub_list in extracted_text if len(sub_list) >= 2]

# # 最後の要素を抽出
# last_item = [sub_list[-1] for sub_list in extracted_text]

# table = []  # 空のリストを作成

# # ループで各要素を辞書型に変換し、空のリストに追加
# for i in range(len(first_item)):
#     try:
#         third = third_items[i]
#     except IndexError:
#         third = None
#     item = {'first': first_item[i], 'second': second_items[i], 'third': third, 'last': last_item[i]}
#     table.append(item)

# # 結果を表示
# print(table)