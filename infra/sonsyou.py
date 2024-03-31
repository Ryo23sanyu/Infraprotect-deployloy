import re

text = ['⑦剥離・鉄筋露出-d', '⑰その他(分類6:異物混入)-e', '①腐食(大大)-e⑤防食機能の劣化(分類1)-e', '']

# 丸数字を直接列挙
circle_numbers = '①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳㉑㉒㉓㉔㉕㉖'

# リスト内の各文字列に対して処理を行う
for item in text:
    # アルファベット(aからe)と直後に続く特定の丸数字の間にコンマを挿入
    updated_item = re.sub(f'([a-e])([{circle_numbers}])', r'\1,\2', item)
    print(f'更新後の文字列: {updated_item}')