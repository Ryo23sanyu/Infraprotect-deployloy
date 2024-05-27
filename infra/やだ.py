import re

bridge_damage = [{'first': [['橋台[胸壁] Ap0101', '橋台[竪壁] Ac0101', '伸縮装置 Ej0101']], 'second': [['①腐食(大小)-d', '⑤防食機能の劣化(分類1)-e'], ['⑤防食機能の劣化(分類1)-e'], ['⑰その他(分類6:施工不良)-e'], ['⑳漏水・滞水-e']]}]
first_item = [['橋台[胸壁] Ap0101', '橋台[竪壁] Ac0101', '伸縮装置 Ej0101']]

replacement_patterns = {
    "①腐食(小小)-b": "腐食", # 1
    "①腐食(小大)-c": "拡がりのある腐食",
    "①腐食(大小)-d": "板厚減少を伴う腐食",
    "①腐食(大大)-e": "板厚減少を伴う拡がりのある腐食",
    "③ゆるみ・脱落-c": "ボルト、ナットにゆるみ・脱落（●本中●本）",
    "③ゆるみ・脱落-e": "ボルト、ナットにゆるみ・脱落（●本中●本）", # 3
    "④破断-e": "鋼材の破断", # 4
    "⑤防食機能の劣化(分類1)-e": "点錆", # 5
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

# 関数を利用して bridge_damage の second 部分を変換する
def transform_second(second_list):
    transformed = []
    
    #print(second_list)
    for delete5_sublist in second_list:
        change_sevetn_sublist = []
        
        # ①から始まる要素と⑤から始まる要素の除外処理
        if any(one_item.startswith('①') for one_item in delete5_sublist) and any(five_item.startswith('⑤') for five_item in delete5_sublist):
            delete5_sublist = [onetofive_item for onetofive_item in delete5_sublist if not onetofive_item.startswith('⑤')]
        print(delete5_sublist)
        
        for sevetn_item in delete5_sublist:
            #print(sevetn_item)
            # replacement_patterns辞書で置換する
            if sevetn_item in replacement_patterns:
                replaced_item = replacement_patterns[sevetn_item]
                change_sevetn_sublist.append(replaced_item)
            else:
                # ⑰から始まる要素の場合、分類の文字を抽出
                if sevetn_item.startswith('⑰'):
                    match = re.search(r"⑰.*?\(.*?:(.*?)\)-e", sevetn_item)
                    # match = re.search(r"⑰その他\(分類6:(.*?)\)-e", item)
                    if match:
                        extracted_text = match.group(1)
                        change_sevetn_sublist.append(extracted_text)
                    else:
                        change_sevetn_sublist.append(sevetn_item)
                else:
                    change_sevetn_sublist.append(sevetn_item)
        
        transformed.append(change_sevetn_sublist)
    
    return transformed

# bridge_damageの second を変換
transformed_second = transform_second(bridge_damage[0]['second'])

# first_item と合成
combined_list = [{'first': first_item, 'second': transformed_second}]
print(combined_list)
