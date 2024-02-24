first = ['横桁 Cr0803', '主桁 Mg0901', '横桁 Cr0801']
second = [['⑦-d'], ['⑰-e'], ['⑦-d']]
third = ['写真番号-15', '写真番号-13,14', '写真番号-17']

table = []  # 空のリストを作成

# ループで各要素を辞書型に変換し、空のリストに追加
for i in range(len(first)):
    item = {'first': first[i], 'second': second[i][0], 'third': third[i]}
    table.append(item)

# 結果を表示
print(table)