# @title デフォルトのタイトル テキスト
# C:\work\django\myproject\myvenv\Scripts\python.exe
import ezdxf
from ezdxf.entities.mtext import MText

dxf = ezdxf.readfile(R'C:\work\django\myproject\myvenv\Infraproject\uploads\12_損傷橋.dxf') # ファイルにアップロードしたdxfファイル名

cad_read = []
for entity in dxf.entities:
    if type(entity) is MText: # or type(entity) is Text: MTextとTextが文字列を表す(https://ymt-lab.com/post/2021/ezdxf-read-dxf-file/)
        cad =  entity.plain_text() # plain_text(読める文字)に変換
        cad_data = cad.split("\n") if len(cad) > 0 else [] # .split():\nの箇所で配列に分配
        if len(cad_data) > 0 and "\n" in cad and not cad.startswith("※") and not any(keyword in cad for keyword in ["×", "."]):
             # 改行を含むかどうかをチェックする:# 特定の文字列で始まるかどうかをチェックする: # 特定の文字を含むかどうかをチェックする
                cad_read.append(cad_data)

print(cad_read)
# 先頭の要素を抽出
first_item = [sub_list[0] for sub_list in cad_read]
# print(f"先頭の要素: {first_item}")
# print()#改行用
# それ以外の要素を抽出
other_items = [sub_list[1:-1] for sub_list in cad_read]
# print(f"それ以外の要素: {other_items}")
# print()#改行用
# 最後の要素を抽出
last_item = [sub_list[-1] for sub_list in cad_read]
# print(f"最後の要素: {last_item}")

# first = ['横桁 Cr0803', '主桁 Mg0901', '横桁 Cr0801']
# second = [['⑦-d'], ['⑰-e'], ['⑦-d']]
# third = ['写真番号-15', '写真番号-13,14', '写真番号-17']

table = []  # 空のリストを作成

# ループで各要素を辞書型に変換し、空のリストに追加
for i in range(len(first_item)):
    item = {'first': first_item[i], 'second': other_items[i], 'third': last_item[i]}
    table.append(item)

# 結果を表示
print(table)