import re
from markupsafe import Markup

# 初期データ
first_item = [Markup('横桁 Cr0803'), Markup('主桁 Mg0901'), Markup('横桁 Cr0201,0301,0402,</br>0403,0602,0604,</br>0704'), Markup('床版 Ds0201,0203'), Markup('排水管 Dp0201,0202'), Markup('横桁 Cr0801'), Markup('排水管 Dp0101'), Markup('横桁 Cr0802'), Markup('床版 Ds0803'), Markup('横桁 Cr0503'), Markup('横桁 Cr0401'), Markup('床版 Ds0101'), Markup('横桁 Cr0102'), Markup('横桁 Cr0103'), Markup('排水管 Dp0102'), Markup('横桁 Cr0304'), Markup('横桁 Cr0204'), Markup('横桁 Cr0101'), Markup('主桁 Mg0901'), Markup('地覆 Fg0201'), Markup('橋台[胸壁] Ap0102,</br>橋台[竪壁] Ac0102,</br>伸縮装置 Ej0102'), Markup('橋台[胸壁] Ap0101,</br>橋台[竪壁] Ac0101,</br>伸縮装置 Ej0101'), Markup('排水ます Dr0101'), Markup('防護柵 Gf0101'), Markup('防護柵 Gf0101'), Markup('防護柵 Gf0101'), Markup('舗装 Pm0101'), Markup('防護柵 Gf0201'), Markup('舗装 Pm0201'), Markup('舗装 Pm0201'), Markup('舗装 Pm0201'), Markup('舗装 Pm0101,0201'), Markup('支承本体 Bh0102,</br>沓座モルタル Bm0102'), Markup('PC定着部 Cn1203'), Markup('排水ます Dr0102,0201,0202')]
second_items = [['⑦剥離・鉄筋露出-d'], ['⑰その他(分類6:異物混入)-e'], ['⑦剥離・鉄筋露出-d'], ['⑦剥離・鉄筋露出-d'], ['①腐食(小大)-c', '⑤防食機能の劣化(分類1)-e'], ['⑦剥離・鉄筋露出-d'], ['①腐食(大大)-e', '⑤防食機能の劣化(分類1)-e'], ['⑦剥離・鉄筋露出-d'], ['⑦剥離・鉄筋露出-d'], ['⑦剥離・鉄筋露出-d', '⑰その他(分類6:施工不良)-e'], ['⑦剥離・鉄筋露出-e'], ['⑦剥離・鉄筋露出-d'], ['⑰その他(分類6:施工不良)-e'], ['⑦剥離・鉄筋露出-e'], ['①腐食(小大)-c', '⑤防食機能の劣化(分類1)-e'], ['⑦剥離・鉄筋露出-e'], ['⑦剥離・鉄筋露出-e'], ['⑰その他(分類6:施工不良)-e'], ['⑦剥離・鉄筋露出-c'], ['⑫うき-e'], ['⑳漏水・滞水-e'], ['⑳漏水・滞水-e'], ['⑰その他(分類6:埋没)-e'], ['⑦剥離・鉄筋露出-d'], ['⑦剥離・鉄筋露出-c'], ['⑦剥離・鉄筋露出-d'], ['㉔土砂詰まり-e'], ['⑦剥離・鉄筋露出-c'], ['㉔土砂詰まり-e'], ['⑮舗装の異常-e'], ['⑮舗装の異常-e'], ['⑮舗装の異常-e'], None, None, ['⑰その他(分類6:埋没)-e']]

bridge_damage = [] # すべての"bridge"辞書を格納するリスト

for i in range(len(first_item)):
    bridge = {
        "first": first_item[i],
        "second": second_items[i] if i < len(second_items) else None  # second_itemsが足りない場合にNoneを使用
    }
    bridge_damage.append(bridge)

replacement_patterns = {
    "①腐食(小小)-b": "腐食",
    "①腐食(小大)-c": "拡がりのある腐食",
    "①腐食(大小)-d": "板厚減少を伴う腐食",
    "①腐食(大大)-e": "板厚減少を伴う拡がりのある腐食",
    "⑦剥離・鉄筋露出-c": "コンクリートの剥離",
    "⑦剥離・鉄筋露出-d": "鉄筋露出",
    "⑦剥離・鉄筋露出-e": "断面減少のある鉄筋露出",
    "⑮舗装の異常-c": "最大幅0.0mmのひびわれ",
    "⑮舗装の異常-e": "最大幅0.0mmのひびわれ・舗装の土砂化",
    "⑳漏水・滞水-e": "漏水・滞水",
    "㉔土砂詰まり-e": "土砂詰まり",
}

pavement_items = []
for bridge in bridge_damage:
    for name_text in first_item:
        pavement_items.append(str(name_text))

    updated_second_items = []  # 更新されたsecond_itemsを格納するための新しいリスト

    for items in second_items:
        if items is None:
            updated_second_items.append(items)
            continue

        # '①'で始まる要素があるか確認
        has_item_starting_with_1 = any(item.startswith('①') for item in items)

        # '①'で始まる要素がある場合、'⑤'で始まる要素を削除
        if has_item_starting_with_1:
            updated_items = [item for item in items if not item.startswith('⑤')]
        else:
            updated_items = items.copy()  # items自体を直接変更しないためのコピー

        # '⑰'で始まる要素があるか確認
        if any(item.startswith('⑰') for item in updated_items):
            new_sublist = []
            # '⑰'で始まる要素がある場合、'⑰'のカッコ内の値のみ抽出
            for item in updated_items:
                if item.startswith('⑰'):
                    match = re.search(r'(?<=:)(.*?)(?=\)-e)', item)
                    if match:
                        new_sublist.append(match.group(1))
                    else:
                        new_sublist.append(item)  # マッチしなかった場合は元のアイテムを保持
                else:
                    new_sublist.append(item)  # '⑰'で始まらないアイテムはそのまま追加
            updated_items = new_sublist  # 更新されたサブリストを反映

        updated_second_items.append(updated_items)
            

# 処理結果を確認
# first_itemとsecond_itemsを組み合わせて結果を表示する
combined_list = []
for i in range(len(first_item)):
    # second_itemsのリストが存在するか、またはNoneであるかをチェック
    second = updated_second_items[i] if i < len(updated_second_items) else None
    
    # 組み合わせをリストに追加
    combined = {"first": first_item[i], "second": second}
    combined_list.append(combined)

# 結果の印刷
damage_memo_list = []
for item in combined_list:
    # item['first']のスペースまでの文字を抽出
    first_part = ""
    clean_text = str(item['first']).replace("</br>", "")
    if "," in clean_text:
        pattern = ',(\d|,)*(?=\s|$)' # 「,」の後に(「数字」か「,」)の場合
        # 条件に一致するかチェック
        if re.search(pattern, clean_text):
            first_part = clean_text.split(" ")[0]
        else:
            sub_pattern = r'[A-Za-z0-9/ /]'
            # 置換処理を行い、日本語のみ抽出
            result = re.sub(sub_pattern, '', clean_text)
            first_part = result  # 数字、アルファベット、コンマを削除
    else:
        first_part = clean_text.split(" ")[0]
    
    # item['second']を置換
    second_parts = []
    if item['second'] is not None:
        for element in item['second']:
            if element in replacement_patterns:
                second_parts.append(replacement_patterns[element])
            else:
                second_parts.append(element)
    
    # second_partsが複数要素を持つ可能性も考えられるので、','.join()で文字列に変換
    second_part_joined = ', '.join(second_parts)
    
    # 結果の表示
    if item['second'] == None:
        combined_data = None
    else:
        combined_data = f"{first_part}に{second_part_joined}が見られる。"
    
    revised_item = {'textarea_content': combined_data}
    damage_memo_list.append(revised_item)
    
for item in damage_memo_list: # views
    print(item) # views