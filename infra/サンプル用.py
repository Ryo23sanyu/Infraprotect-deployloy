# << 材料の置換 >>

# 置換マッピング
replace_dict = {
    '鋼': 'S',
    'コンクリート': 'C',
    'その他': 'X'
}

text = "鋼,コンクリート"

# テキストをカンマで分割します。
elements = text.split(',')

# それぞれの要素を置換辞書に基づいて変換します。
replaced_elements = [replace_dict.get(element, element) for element in elements]

# 変換された要素を再びカンマで結合します。
replaced_text = ','.join(replaced_elements)

print(replaced_text)