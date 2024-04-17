# 元のテキストデータ
text = "※特記なき損傷\n横桁 Cr0102 ①-d\n横桁 Cr0201,0301,0402 ⑦-d\n床版 Ds0101～0108 ⑪-c"

# 改行でテキストを分割してリスト化
lines = text.split('\n')

# 各行をサブリストとして持つ多重リストを構築
text_list = [[line] for line in lines]

# 結果の確認
print(text_list)