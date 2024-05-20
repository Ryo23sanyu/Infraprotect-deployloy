parts = ['主桁 Mg0110', '床版 Ds0101']
first_part = ['主桁', '床版']
join_damagename_result = ['⑧漏水・遊離石灰-e', '⑦剥離・鉄筋露出-d,⑪床版ひびわれ-d']
changed_damage_name = []

replacement_patterns = {
    "①腐食(小小)-b": "腐食", # 1
    "①腐食(小大)-c": "拡がりのある腐食",
    "①腐食(大小)-d": "板厚減少を伴う腐食",
    "①腐食(大大)-e": "板厚減少を伴う拡がりのある腐食",
    "③ゆるみ・脱落-c": "ボルト、ナットにゆるみ・脱落（●本中●本）",
    "③ゆるみ・脱落-e": "ボルト、ナットにゆるみ・脱落（●本中●本）", # 3
    "④破断-e": "鋼材の破断", # 4
    "⑥ひびわれ(小小)-b": "最大幅0.0mmのひびわれ", # 6
    "⑥ひびわれ(小大)-c": "最大幅0.0mmかつ間隔0.5m未満のひびわれ",
    "⑥ひびわれ(中小)-c": "最大幅0.0mmのひびわれ",
    "⑥ひびわれ(中大)-d": "最大幅0.0mmかつ間隔0.5m未満のひびわれ",
    "⑥ひびわれ(大小)-d": "最大幅0.0mmのひびわれ",
    "⑥ひびわれ(大大)-e": "最大幅0.0mmかつ間隔0.5m未満のひびわれ",
    "⑦剥離・鉄筋露出-c": "コンクリートの剥離", # 7
    "⑦剥離・鉄筋露出-d": "鉄筋露出",
    "⑦剥離・鉄筋露出-e": "断面減少を伴う鉄筋露出",
    "⑧漏水・遊離石灰-c": "漏水", # 8
    "⑧漏水・遊離石灰-d": "遊離石灰",
    "⑧漏水・遊離石灰-e": "著しい遊離石灰・泥や錆汁の混入を伴う漏水",
    "⑨抜け落ち-e": "コンクリート塊の抜け落ち", # 9
    "⑪床版ひびわれ-b": "最大幅0.0mmの1方向ひびわれ",
    "⑪床版ひびわれ-c": "最大幅0.0mmの1方向ひびわれ",
    "⑪床版ひびわれ-d": "最大幅0.0mmの1方向ひびわれ",
    "⑪床版ひびわれ-e": "最大幅0.0mmの角落ちを伴う1方向ひびわれ", # 11
    "⑫うき-e": "コンクリートのうき", # 12
    "⑮舗装の異常-c": "最大幅0.0mmのひびわれ",
    "⑮舗装の異常-e": "最大幅0.0mmのひびわれ・舗装の土砂化", # 15
    "⑯定着部の異常-c": "定着部の損傷。",
    "⑯定着部の異常(分類2)-e": "定着部の著しい損傷", # 16
    "⑳漏水・滞水-e": "漏水・滞水", # 20
    "㉓変形・欠損-c": "変形・欠損", # 23
    "㉓変形・欠損-e": "著しい変形・欠損",
    "㉔土砂詰まり-e": "土砂詰まり", # 24
}

# 置換パターンに基づいて置換する関数を定義
def replace_patterns(text, patterns):
    for old, new in patterns.items():
        text = text.replace(old, new)
    return text

# 損傷文字を置換
for damage in join_damagename_result:
    changed_damage_name.append(replace_patterns(damage, replacement_patterns))

# 1つ目の要素の損傷メモ
combined_result = f"{first_part[0]}に{changed_damage_name[0]}が見られる。"
# 2つ目の要素の損傷メモ
combined_result += f"また、{first_part[1]}に{changed_damage_name[1]}"
# 2つ目以降の要素を結合
if len(first_part) >= 3:
    for i in range(2, len(first_part)):
        combined_result += f"、{first_part[i]}に{changed_damage_name[i]}"
else:
    None
if len(first_part) >= 2:
    combined_result += "が見られる。"

# 関連損傷をつけるコード
# 1つ目の要素にカンマがあるかどうかをチェック
if "," in join_damagename_result[0]:
    # カンマがある場合、1つ目のpartsと1つ目のjoin_damagename_resultを結合し、残りはそのまま結合
    tokki_1 = f"\n【関連損傷】\n{parts[0]}:{join_damagename_result[0]}"
    for i in range(1, len(parts)):
        tokki_1 += f"、{parts[i]}:{join_damagename_result[i]}"
else:
    # カンマがない場合、2つ目以降のpartsとjoin_damagename_resultを結合
    tokki_1 = "\n【関連損傷】\n"
    for i in range(len(parts)):
        if i > 0:
            if tokki_1:
                tokki_1 += ""
            tokki_1 += f"{parts[i]}:{join_damagename_result[i]}、"
combined_result += tokki_1
print(combined_result[:-1])