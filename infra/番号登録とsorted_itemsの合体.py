import re


number_create = [{'parts_name': ['主桁'], 'number': ['0401'], 'material': ['コンクリート'], 'main_frame': ['〇']}, 
                 {'parts_name': ['主桁'], 'number': ['0701'], 'material': ['コンクリート'], 'main_frame': ['✕']}]

flattened_join = [{'parts_name': ['主桁 Mg0101'], 'damage_name': ['⑦剥離・鉄筋露出-d'], 'this_time_picture': None}, {'parts_name': ['主桁 Mg0102'], 'damage_name': ['⑦剥離・鉄筋露出-d'], 'this_time_picture': None}, {'parts_name': ['主桁 Mg0103'], 'damage_name': ['⑦剥離・鉄筋露出-d'], 'this_time_picture': None}, {'parts_name': ['主桁 Mg0104'], 'damage_name': ['⑦剥離・鉄筋露出-d'], 'this_time_picture': None}, {'parts_name': ['主桁 Mg0201'], 'damage_name': ['⑦剥離・鉄筋露出-d'], 'this_time_picture': None}, {'parts_name': ['主桁 Mg0202'], 'damage_name': ['⑦剥離・鉄筋露出-d'], 'this_time_picture': None}, 
                  {'parts_name': ['主桁 Mg0203'], 'damage_name': ['⑦剥離・鉄筋露出-d'], 'this_time_picture': None}, {'parts_name': ['主桁 Mg0204'], 'damage_name': ['⑦剥離・鉄筋露出-d'], 'this_time_picture': None}, {'parts_name': ['主桁 Mg0302'], 'damage_name': ['⑦剥離・鉄筋露出-d'], 'this_time_picture': None}, {'parts_name': ['主桁 Mg0304'], 'damage_name': ['⑦剥離・鉄筋露出-d'], 'this_time_picture': None}, {'parts_name': ['主桁 Mg0401'], 'damage_name': ['⑦剥離・鉄筋露出-d'], 'this_time_picture': None}, {'parts_name': ['主桁 Mg0402'], 'damage_name': ['⑦剥離・鉄筋露出-d'], 'this_time_picture': None}, 
                  {'parts_name': ['主桁 Mg0403'], 'damage_name': ['⑦剥離・鉄筋露出-d'], 'this_time_picture': None}, {'parts_name': ['主桁 Mg0901'], 'damage_name': ['⑦剥離・鉄筋露出-c'], 'this_time_picture': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070537.JPG']}, {'parts_name': ['主桁 Mg0901'], 'damage_name': ['⑰その他(分類6:異物混入)-e'], 'this_time_picture': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070404.JPG']}, {'parts_name': ['横桁 Cr0101'], 'damage_name': ['⑰その他(分類6:施工不良)-e'], 'this_time_picture': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070496.JPG']}, 
                  {'parts_name': ['横桁 Cr0102'], 'damage_name': ['⑰その他(分類6:施工不良)-e'], 'this_time_picture': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070424.JPG', 'infra/img\\9月7日\u3000佐藤\u3000地上\\P9070430.JPG']}, {'parts_name': ['横桁 Cr0103'], 'damage_name': ['⑦剥離・鉄筋露出-e'], 'this_time_picture': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070433.JPG']}, {'parts_name': ['横桁 Cr0201'], 'damage_name': ['⑦剥離・鉄筋露出-d'], 'this_time_picture': None}, {'parts_name': ['横桁 Cr0301'], 'damage_name': ['⑦剥離・鉄筋露出-d'], 'this_time_picture': None}, {'parts_name': ['横桁 Cr0402'], 'damage_name': ['⑦剥離・鉄筋露出-d'], 'this_time_picture': None},
                  {'parts_name': ['横桁 Cr0403'], 'damage_name': ['⑦剥離・鉄筋露出-d'], 'this_time_picture': None}, {'parts_name': ['横桁 Cr0602'], 'damage_name': ['⑦剥離・鉄筋露出-d'], 'this_time_picture': None}, {'parts_name': ['横桁 Cr0604'], 'damage_name': ['⑦剥離・鉄筋露出-d'], 'this_time_picture': None}, {'parts_name': ['横桁 Cr0704'], 'damage_name': ['⑦剥離・鉄筋露出-d'], 'this_time_picture': None}, {'parts_name': ['横桁 Cr0204'], 'damage_name': ['⑦剥離・鉄筋露出-e'], 'this_time_picture': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070478.JPG']}, {'parts_name': ['横桁 Cr0304'], 'damage_name': ['⑦剥離・鉄筋露出-e'], 'this_time_picture': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070476.JPG']}, 
                  {'parts_name': ['横桁 Cr0401'], 'damage_name': ['⑦剥離・鉄筋露出-e'], 'this_time_picture': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070523.JPG']}, {'parts_name': ['横桁 Cr0503'], 'damage_name': ['⑦剥離・鉄筋露出-d', '⑰その他(分類6:施工不良)-e'], 'this_time_picture': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070450.JPG', 'infra/img\\9月7日\u3000佐藤\u3000地上\\P9070452.JPG']}, {'parts_name': ['横桁 Cr0801'], 'damage_name': ['⑦剥離・鉄筋露出-d'], 'this_time_picture': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070525.JPG']}, {'parts_name': ['横桁 Cr0802'], 'damage_name': ['⑦剥離・鉄筋露出-d'], 'this_time_picture': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070396.JPG', 'infra/img\\9月7日\u3000佐藤\u3000地上\\P9070412.JPG']}, 
                  {'parts_name': ['横桁 Cr0803'], 'damage_name': ['⑦剥離・鉄筋露出-d'], 'this_time_picture': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070458.JPG']}, {'parts_name': ['床版 Ds0101'], 'damage_name': ['⑦剥離・鉄筋露出-d'], 'this_time_picture': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070497.JPG']}, {'parts_name': ['床版 Ds0201'], 'damage_name': ['⑦剥離・鉄筋露出-d'], 'this_time_picture': None}, {'parts_name': ['床版 Ds0203'], 'damage_name': ['⑦剥離・鉄筋露出-d'], 'this_time_picture': None}, {'parts_name': ['床版 Ds0803'], 'damage_name': ['⑦剥離・鉄筋露出-d'], 'this_time_picture': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070465.JPG']}, 
                  {'parts_name': ['PC定着部 Cn1203'], 'damage_name': ['NON-a'], 'this_time_picture': None}, {'parts_name': ['橋台[胸壁] Ap0101'], 'damage_name': ['⑳漏水・滞水-e'], 'this_time_picture': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070438.JPG']}, {'parts_name': ['橋台[竪壁] Ac0101'], 'damage_name': ['⑳漏水・滞水-e'], 'this_time_picture': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070438.JPG']}, {'parts_name': ['伸縮装置 Ej0101'], 'damage_name': ['⑳漏水・滞水-e'], 'this_time_picture': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070438.JPG']}, {'parts_name': ['橋台[胸壁] Ap0102'], 'damage_name': ['⑳漏水・滞水-e'], 'this_time_picture': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070443.JPG']}, 
                  {'parts_name': ['橋台[竪壁] Ac0102'], 'damage_name': ['⑳漏水・滞水-e'], 'this_time_picture': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070443.JPG']}, {'parts_name': ['伸縮装置 Ej0102'], 'damage_name': ['⑳漏水・滞水-e'], 'this_time_picture': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070443.JPG']}, {'parts_name': ['支承本体 Bh0102'], 'damage_name': ['NON-a'], 'this_time_picture': None}, {'parts_name': ['沓座モルタル Bm0102'], 'damage_name': ['NON-a'], 'this_time_picture': None}, {'parts_name': ['地覆 Fg0201'], 'damage_name': ['⑫うき-e'], 'this_time_picture': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070535.JPG']}, 
                  {'parts_name': ['排水管 Dp0101'], 'damage_name': ['①腐食(大大)-e', '⑤防食機能の劣化(分類1)-e'], 'this_time_picture': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070422.JPG']}, {'parts_name': ['排水管 Dp0102'], 'damage_name': ['①腐食(小大)-c', '⑤防食機能の劣化(分類1)-e'], 'this_time_picture': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070486.JPG']}, {'parts_name': ['排水管 Dp0201'], 'damage_name': ['①腐食(小大)-c', '⑤防食機能の劣化(分類1)-e'], 'this_time_picture': None}, {'parts_name': ['排水管 Dp0202'], 'damage_name': ['①腐食(小大)-c', '⑤防食機能の劣化(分類1)-e'], 'this_time_picture': None}]

split_parts_and_damage = []

# 各要素に対して処理を行う
for item in flattened_join:
    combined_string = item['parts_name'][0]
    
    # 正規表現を使って、記号と数字の部分で分割する
    match = re.match(r'(.+ [A-Za-z]+)(\d+)', combined_string)
    
    if match:
        parts_name = match.group(1)
        number = match.group(2)
        
        for damage in item['damage_name']:
            if "-" in damage:
                damage_name, damage_lank = damage.split("-")
            
            parts_dict = {
                'parts_name': [parts_name],
                'number': [number],
                'damage_name': [damage_name],
                'damage_lank': [damage_lank],
                'this_time_picture': item['this_time_picture']  # this_time_pictureを追加
            }
            split_parts_and_damage.append(parts_dict)
            
# 分解
# print(f"split_parts_and_damage：{split_parts_and_damage}")


order_lank = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}

# 一時的な辞書を作成
temp_dict = {}

for part in split_parts_and_damage:
    key = (tuple(part['parts_name']), tuple(part['number']), tuple(part['damage_name']), tuple(part['this_time_picture']) if part['this_time_picture'] else ())
                                                                                         # Noneのときはtupleが使えないため　↑
    if key not in temp_dict:
        temp_dict[key] = set()
    temp_dict[key].update(part['damage_lank'])

# 集約した情報から重複を削除したリストを作成
sorted_split = []
for key, damage_lank_set in temp_dict.items():
    damage_lank_list = sorted(damage_lank_set, key=lambda x: order_lank[x])
    sorted_split.append({
        'parts_name': list(key[0]),
        'number': list(key[1]),
        'damage_name': list(key[2]),
        'damage_lank': damage_lank_list,
        'this_time_picture': list(key[3]) if key[3] else None
              # tupleが使えないため空、空のときはNoneを返す　↑
    })

#print(f"sorted_split：{sorted_split}")

# 置換マッピング
replace_dict = {
    '鋼': 'S',
    'コンクリート': 'C',
    'その他': 'X'
}

# 置換処理
for part in number_create:
    part['material'] = [replace_dict.get(mat, mat) for mat in part['material']]

# print(number_create)

# 結果格納用のリスト
result = []

# sorted_splitをループし、number_createと比較
for item in sorted_split:
    found = False
    for nc_item in number_create:
        if item['parts_name'] == nc_item['parts_name'] and item['number'] == nc_item['number']:
            item.update({'material': nc_item['material'], 'main_frame': nc_item['main_frame']})
            found = True
            break
    if 'material' not in item:
        item['material'] = None
    if 'main_frame' not in item:
        item['main_frame'] = None
    result.append(item)

# number_createの項目を結果に追加
for nc_item in number_create:
    # sorted_splitに存在しない場合のチェック
    exists = any(item['parts_name'] == nc_item['parts_name'] and item['number'] == nc_item['number'] for item in sorted_split)
    if not exists:
        result.append({'parts_name': nc_item['parts_name'], 'number': nc_item['number'], 'material': nc_item['material'], 'main_frame': nc_item['main_frame'], 'this_time_picture': None})

# 指定した順番でキーを整列
ordered_result = []
ordered_keys = ['parts_name', 'number', 'material', 'damage_lank', 'damage_name', 'main_frame', 'this_time_picture']

for item in result:
    ordered_item = {key: item.get(key) for key in ordered_keys}
    ordered_result.append(ordered_item)

# 結果の表示
print(f"ordered_result:{ordered_result}")