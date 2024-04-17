import re

# 正規表現パターン

# リストのデータ
extracted_text = [['主桁 Mg0101', '①-d', '地覆 Fg0101,0401', '㉓変形・欠損-c', '舗装 Pm0101～0301', '㉔土砂詰まり-e', \
  '写真番号-00', 'defpoints'], ['主桁 Mg0902', '⑦-c', '写真番号-00', 'defpoints']]

# 正規表現を使ってパターンに一致する要素だけを取り出す
pattern = r'[\u2460-\u3256].*-[a-zA-Z]'
filtered_items = [[item for item in sub_list if re.match(pattern, item)] for sub_list in extracted_text]
print(filtered_items)# [['①-d', '㉓変形・欠損-c']]

# 「日本語」、「スペース」、「アルファベット」、「4桁以上の数字」
pattern = r'[ぁ-んァ-ヶｱ-ﾝﾞﾟ一-龠]+\s+[a-zA-Z]+\d{4,}'
super_text = [[item for item in sub_list if re.match(pattern, item)] for sub_list in extracted_text]
print(super_text)# [['主桁 Mg0101', '地覆 Fg0101,0401', '舗装 Pm0101～0301']]