import re

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

bridge_damage = [{'first': [['排水ます Dr0101']], 'second': [['⑰その他(分類6:埋没)-e']]}]
first_item = [[['排水ます Dr0102', '排水ます Dr0201', '排水ます Dr0202']]]

def replace_patterns(text, patterns):
    for key, value in patterns.items():
        text = re.sub(key, value, text)
    return text

pavement_items = []

for damage_parts in bridge_damage:
    # print(damage_parts)
    if isinstance(damage_parts["second"], list):  # "second"がリストの場合
        filtered_second_items = []
        for sublist in damage_parts["second"]:
            if isinstance(sublist, list):  # サブリストがリストである場合
                if any(item.startswith('①') for item in sublist) and any(item.startswith('⑤') for item in sublist):
                    # ⑤で始まる要素を取り除く
                    filtered_sublist = [item for item in sublist if not item.startswith('⑤')]
                    filtered_second_items.append(filtered_sublist)
                elif any(item.startswith('⑰') for item in sublist):
                            # サブリスト内の全アイテムを再度チェック
                            seventn = []
                            for item in sublist:
                                if item.startswith('⑰'):
                                    match = re.search(r"⑰.*?\(.*?:(.*?)\)-e", item)
                                    if match:
                                        extracted_text = match.group(1)
                                        seventn.append(extracted_text)
                            filtered_second_items.append(seventn)
                else:
                    filtered_second_items.append(sublist)
            else:
                filtered_second_items.append([sublist])
        
        # フィルタリング後のsecond_itemsに対して置換を行う
        replaced_items = []
        for sublist in filtered_second_items:
            replaced_sublist = [replace_patterns(item, replacement_patterns) for item in sublist]
            replaced_items.append(replaced_sublist)
        
        combined = {"first": first_item, "second": replaced_items}
        print(combined)