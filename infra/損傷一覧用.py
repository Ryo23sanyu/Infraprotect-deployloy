from collections import OrderedDict, defaultdict
import pprint
import re

sorted_items = [
    {'parts_name': [['横桁 Cr0102']], 'damage_name': [['⑰その他(分類6:施工不良)-e']], 
     'join': [{'parts_name': ['横桁 Cr0102'], 'damage_name': ['⑰その他(分類6:施工不良)-e']}], 
     'picture_number': '写真番号-4,5', 'this_time_picture': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070424.JPG', 'infra/img\\9月7日\u3000佐藤\u3000地上\\P9070430.JPG'], 
     'last_time_picture': None, 
     'textarea_content': '横桁に施工不良が見られる。', 
     'damage_coordinate': ['532578.7587482664', '229268.8593029478'], 'picture_coordinate': ['532985.6409545547', '228954.2335446222']}
    ,
    {'parts_name': [['床版 Ds0201', '床版 Ds0203']], 'damage_name': [['⑦剥離・鉄筋露出-d']], 
     'join': [{'parts_name': ['床版 Ds0201'], 'damage_name': ['⑦剥離・鉄筋露出-d']}, {'parts_name': ['床版 Ds0203'], 'damage_name': ['⑦剥離・鉄筋露出-d']}], 
     'picture_number': None, 'this_time_picture': None, 
     'last_time_picture': None, 
     'textarea_content': '床版に鉄筋露出が見られる。 \n【関連損傷】\n床版 Ds0203:⑦剥離・鉄筋露出-d', 
     'damage_coordinate': ['525003.839727268', '213095.7270112425'], 'picture_coordinate': None}
    ,
    {'parts_name': [['床版 Ds0201', '床版 Ds0203']], 'damage_name': [['⑦剥離・鉄筋露出-d']], 
     'join': [{'parts_name': ['床版 Ds0201'], 'damage_name': ['⑦剥離・鉄筋露出-d']}, {'parts_name': ['床版 Ds0203'], 'damage_name': ['⑦剥離・鉄筋露出-d']}], 
     'picture_number': None, 'this_time_picture': None, 
     'last_time_picture': None, 
     'textarea_content': '床版に鉄筋露出が見られる。 \n【関連損傷】\n床版 Ds0203:⑦剥離・鉄筋露出-d', 
     'damage_coordinate': ['525003.839727268', '213095.7270112425'], 'picture_coordinate': None}
    ,
    {'parts_name': [['橋台[胸壁] Ap0101', '橋台[竪壁] Ac0101', '伸縮装置 Ej0101']], 'damage_name': [['⑳漏水・滞水-e']], 
     'join': [{'parts_name': ['橋台[胸壁] Ap0101'], 'damage_name': ['⑳漏水・滞水-e']}, {'parts_name': ['橋台[竪壁] Ac0101'], 'damage_name': ['⑳漏水・滞水-e']}, {'parts_name': ['伸縮装置 Ej0101'], 'damage_name': ['⑳漏水・滞水-e']}], 
     'picture_number': '写真番号-18', 'this_time_picture': ['infra\img\9月7日　佐藤　地上\P9070438.JPG'], 
     'last_time_picture': 'media\P6100002.JPG', 
     'textarea_content': '橋台[胸壁]および橋台[竪壁],伸縮装置に漏水・滞水が見られる。 \n【関連損傷】\n橋台[竪壁] Ac0101,伸縮装置 Ej0101:⑳漏水・滞水-e', 
     'damage_coordinate': ['535305.6406762057', '190342.4721676922'], 'picture_coordinate': ['537494.8440878117', '190371.7813098583']}
    ,
    {'parts_name': [['橋台[胸壁] Ap0101', '橋台[竪壁] Ac0101', '伸縮装置 Ej0101']], 'damage_name': [['⑳漏水・滞水-e']], 
     'join': [{'parts_name': ['橋台[胸壁] Ap0101'], 'damage_name': ['⑳漏水・滞水-e']}, {'parts_name': ['橋台[竪壁] Ac0101'], 'damage_name': ['⑳漏水・滞水-e']}, {'parts_name': ['伸縮装置 Ej0101'], 'damage_name': ['⑳漏水・滞水-e']}], 
     'picture_number': '写真番号-18', 'this_time_picture': ['infra\img\9月7日　佐藤　地上\P9070438.JPG'], 
     'last_time_picture': 'media\P6100020.JPG', 
     'textarea_content': '橋台[胸壁]および橋台[竪壁],伸縮装置に漏水・滞水が見られる。 \n【関連損傷】\n橋台[竪壁] Ac0101,伸縮装置 Ej0101:⑳漏水・滞水-e', 
     'damage_coordinate': ['535305.6406762057', '190342.4721676922'], 'picture_coordinate': ['537494.8440878117', '190371.7813098583']}
    ,
    {'parts_name': [['支承本体 Bh0101'], ['沓座モルタル Bm0101']], 'damage_name': [['①腐食(小小)-b', '⑤防食機能の劣化(分類1)-e', '㉓変形・欠損-c'], ['⑦剥離・鉄筋露出-c']], 
     'join': [{'parts_name': ['支承本体 Bh0101'], 'damage_name': ['①腐食(小小)-b', '⑤防食機能の劣化(分類1)-e', '㉓変形・欠損-c']}, {'parts_name': ['沓座モルタル Bm0101'], 'damage_name': ['⑦剥離・鉄筋露出-c']}], 
     'picture_number': '写真番号-27', 'this_time_picture': ['infra\img\9月7日　佐藤　地上\P9070504.JPG'], 
     'last_time_picture': None, 
     'textarea_content': '支承本体に腐食,変形・欠損が見られる。また沓座モルタルにコンクリートの剥離が見られる。 \n【関連損傷】\n支承本体 Bh0101:㉓変形・欠損-c, 沓座モルタル Bm0101:⑦剥離・鉄筋露出-c', 
     'damage_coordinate': ['547050.6408404222', '164535.3885015437'], 'picture_coordinate': ['549493.5416080137', '164259.8990548863']}
    ,
    {'parts_name': [['支承本体 Bh0101'], ['沓座モルタル Bm0101']], 'damage_name': [['①腐食(小小)-b', '⑤防食機能の劣化(分類1)-e', '㉓変形・欠損-c'], ['⑦剥離・鉄筋露出-c']], 
     'join': [{'parts_name': ['支承本体 Bh0101'], 'damage_name': ['①腐食(小小)-b', '⑤防食機能の劣化(分類1)-e', '㉓変形・欠損-c']}, {'parts_name': ['沓座モルタル Bm0101'], 'damage_name': ['⑦剥離・鉄筋露出-c']}], 
     'picture_number': '写真番号-27', 'this_time_picture': ['infra\img\9月7日　佐藤　地上\P9070504.JPG'], 
     'last_time_picture': None, 
     'textarea_content': '支承本体に腐食,変形・欠損が見られる。また沓座モルタルにコンクリートの剥離が見られる。 \n【関連損傷】\n支承本体 Bh0101:㉓変形・欠損-c, 沓座モルタル Bm0101:⑦剥離・鉄筋露出-c', 
     'damage_coordinate': ['547050.6408404222', '164535.3885015437'], 'picture_coordinate': ['549493.5416080137', '164259.8990548863']}
    ,
    {'parts_name': [['排水管 Dp0101']], 'damage_name': [['①腐食(大大)-e', '⑤防食機能の劣化(分類1)-e']], 
     'join': [{'parts_name': ['排水管 Dp0101'], 'damage_name': ['①腐食(大大)-e', '⑤防食機能の劣化(分類1)-e']}], 
     'picture_number': '写真番号-31', 'this_time_picture': ['infra\img\9月7日　佐藤　地上\P9070422.JPG'], 
     'last_time_picture': None, 
     'textarea_content': '排水管に板厚減少を伴う拡がりのある腐食,点錆が見られる。\n【関連損傷】\n排水管 Dp0101:⑤防食機能の劣化(分類1)-e', 
     'damage_coordinate': ['538482.3557216563', '229268.8593029478'], 'picture_coordinate': ['538810.3087944178', '228910.3502713814']}
     ,
    {'parts_name': [['排水管 Dp0102']], 'damage_name': [['①腐食(小大)-c', '⑤防食機能の劣化(分類1)-e']], 
     'join': [{'parts_name': ['排水管 Dp0102'], 'damage_name': ['①腐食(小大)-c', '⑤防食機能の劣化(分類1)-e']}], 
     'picture_number': '写真番号-32', 'this_time_picture': ['infra\img\9月7日　佐藤　地上\P9070486.JPG'], 
     'last_time_picture': None, 
     'textarea_content': '排水管に拡がりのある腐食,点錆が見られる。\n【関連損傷】\n排水管 Dp0102:⑤防食機能の劣化(分類1)-e', 
     'damage_coordinate': ['547059.1990495767', '229268.8593029478'], 'picture_coordinate': ['549204.9604817769', '229256.3408485695']}
    ,
    {'parts_name': [['排水管 Dp0103']], 'damage_name': [['①腐食(大大)-e', '⑤防食機能の劣化(分類1)-e']], 
     'join': [{'parts_name': ['排水管 Dp0101'], 'damage_name': ['①腐食(大大)-e', '⑤防食機能の劣化(分類1)-e']}], 
     'picture_number': '写真番号-31', 'this_time_picture': ['infra\img\9月7日　佐藤　地上\P9070422.JPG'], 
     'last_time_picture': None, 
     'textarea_content': '排水管に板厚減少を伴う拡がりのある腐食,点錆が見られる。\n【関連損傷】\n排水管 Dp0101:⑤防食機能の劣化(分類1)-e', 
     'damage_coordinate': ['538482.3557216563', '229268.8593029478'], 'picture_coordinate': ['538810.3087944178', '228910.3502713814']}
    ,
    {'parts_name': [['排水管 Dp0103']], 'damage_name': [['①腐食(大大)-e', '⑤防食機能の劣化(分類1)-e']], 
     'join': [{'parts_name': ['排水管 Dp0101'], 'damage_name': ['①腐食(大大)-e', '⑤防食機能の劣化(分類1)-e']}], 
     'picture_number': '写真番号-31', 'this_time_picture': ['infra\img\9月7日　佐藤　地上\P9070422.JPG'], 
     'last_time_picture': None, 
     'textarea_content': '排水管に板厚減少を伴う拡がりのある腐食,点錆が見られる。\n【関連損傷】\n排水管 Dp0101:⑤防食機能の劣化(分類1)-e', 
     'damage_coordinate': ['538482.3557216563', '229268.8593029478'], 'picture_coordinate': ['538810.3087944178', '228910.3502713814']}
]

# joinキーのみを抽出
join_values = [item['join'] for item in sorted_items]

# join値を1行にまとめる
flattened_join_values = [join_item for sublist in join_values for join_item in sublist]

# print(flattened_join_values)
flattened_join_values = [{'parts_name': ['横桁 Cr0102'], 'damage_name': ['⑰その他(分類6:施工不良)-e']}, 
                         {'parts_name': ['床版 Ds0201'], 'damage_name': ['⑦剥離・鉄筋露出-d']}, 
                         {'parts_name': ['床版 Ds0203'], 'damage_name': ['⑦剥離・鉄筋露出-d']}, 
                         {'parts_name': ['床版 Ds0201'], 'damage_name': ['⑦剥離・鉄筋露出-d']}, 
                         {'parts_name': ['床版 Ds0203'], 'damage_name': ['⑦剥離・鉄筋露出-d']}, 
                         {'parts_name': ['橋台[胸壁] Ap0101'], 'damage_name': ['⑳漏水・滞水-e']}, {'parts_name': ['橋台[竪壁] Ac0101'], 'damage_name': ['⑳漏水・滞水-e']}, {'parts_name': ['伸縮装置 Ej0101'], 'damage_name': ['⑳漏水・滞水-e']}, 
                         {'parts_name': ['橋台[胸壁] Ap0101'], 'damage_name': ['⑳漏水・滞水-e']}, {'parts_name': ['橋台[竪壁] Ac0101'], 'damage_name': ['⑳漏水・滞水-e']}, {'parts_name': ['伸縮装置 Ej0101'], 'damage_name': ['⑳漏水・滞水-e']}, 
                         {'parts_name': ['支承本体 Bh0101'], 'damage_name': ['①腐食(小小)-b', '⑤防食機能の劣化(分類1)-e', '㉓変形・欠損-c']}, {'parts_name': ['沓座モルタル Bm0101'], 'damage_name': ['⑦剥離・鉄筋露出-c']}, 
                         {'parts_name': ['支承本体 Bh0101'], 'damage_name': ['①腐食(小小)-b', '⑤防食機能の劣化(分類1)-e', '㉓変形・欠損-c']}, {'parts_name': ['沓座モルタル Bm0101'], 'damage_name': ['⑦剥離・鉄筋露出-c']}, 
                         {'parts_name': ['排水管 Dp0101'], 'damage_name': ['①腐食(大大)-e', '⑤防食機能の劣化(分類1)-e']}, 
                         {'parts_name': ['排水管 Dp0102'], 'damage_name': ['①腐食(小大)-c', '⑤防食機能の劣化(分類1)-e']}, 
                         {'parts_name': ['排水管 Dp0101'], 'damage_name': ['①腐食(大大)-e', '⑤防食機能の劣化(分類1)-e']}, 
                         {'parts_name': ['排水管 Dp0101'], 'damage_name': ['①腐食(大大)-e', '⑤防食機能の劣化(分類1)-e']}]


# 新しいリストを作成
split_parts_and_damage = []

# 各要素に対して処理を行う
for item in flattened_join_values:
    combined_string = item['parts_name'][0]
    
    # 正規表現を使って、記号と数字の部分で分割する
    match = re.match(r'(.+ [A-Za-z]+)([0-9]+)', combined_string)
    
    # 辞書形式で格納し、damage_nameごとに分割して格納する
    if match:
        parts_name = [match.group(1)]  # parts_nameをリストに変換
        number = [match.group(2)]      # numberをリストに変換
        for damage in item['damage_name']:
            if "-" in damage:
                damage_name = damage.split("-")[0]
                damage_lank = damage.split("-")[1]
            parts_dict = {
                'parts_name': parts_name,
                'number': number,
                'damage_name': [damage_name],  # damage_nameもリストに変換
                'damage_lank': [damage_lank]  # damage_nameもリストに変換
            }
            split_parts_and_damage.append(parts_dict)

# print(split_parts_and_damage)
split_parts_and_damage = [{'parts_name': ['横桁 Cr'], 'number': ['0102'], 'damage_name': ['⑰その他(分類6:施工不良)'], 'damage_lank': ['e']}, 
                          {'parts_name': ['床版 Ds'], 'number': ['0201'], 'damage_name': ['⑦剥離・鉄筋露出'], 'damage_lank': ['d']}, 
                          {'parts_name': ['床版 Ds'], 'number': ['0203'], 'damage_name': ['⑦剥離・鉄筋露出'], 'damage_lank': ['d']}, 
                          {'parts_name': ['橋台[胸壁] Ap'], 'number': ['0101'], 'damage_name': ['⑳漏水・滞水'], 'damage_lank': ['e']}, 
                          {'parts_name': ['橋台[竪壁] Ac'], 'number': ['0101'], 'damage_name': ['⑳漏水・滞水'], 'damage_lank': ['e']}, 
                          {'parts_name': ['伸縮装置 Ej'], 'number': ['0101'], 'damage_name': ['⑳漏水・滞水'], 'damage_lank': ['e']}, 
                          {'parts_name': ['橋台[胸壁] Ap'], 'number': ['0101'], 'damage_name': ['⑳漏水・滞水'], 'damage_lank': ['e']}, 
                          {'parts_name': ['橋台[竪壁] Ac'], 'number': ['0101'], 'damage_name': ['⑳漏水・滞水'], 'damage_lank': ['e']}, 
                          {'parts_name': ['伸縮装置 Ej'], 'number': ['0101'], 'damage_name': ['⑳漏水・滞水'], 'damage_lank': ['e']}, 
                          {'parts_name': ['支承本体 Bh'], 'number': ['0101'], 'damage_name': ['①腐食(小小)'], 'damage_lank': ['b']}, 
                          {'parts_name': ['支承本体 Bh'], 'number': ['0101'], 'damage_name': ['⑤防食機能の劣化(分類1)'], 'damage_lank': ['e']}, 
                          {'parts_name': ['支承本体 Bh'], 'number': ['0101'], 'damage_name': ['㉓変形・欠損'], 'damage_lank': ['c']}, 
                          {'parts_name': ['沓座モルタル Bm'], 'number': ['0101'], 'damage_name': ['⑦剥離・鉄筋露出'], 'damage_lank': ['c']}, 
                          {'parts_name': ['支承本体 Bh'], 'number': ['0101'], 'damage_name': ['①腐食(小小)'], 'damage_lank': ['b']}, 
                          {'parts_name': ['支承本体 Bh'], 'number': ['0101'], 'damage_name': ['⑤防食機能の劣化(分類1)'], 'damage_lank': ['e']}, 
                          {'parts_name': ['支承本体 Bh'], 'number': ['0101'], 'damage_name': ['㉓変形・欠損'], 'damage_lank': ['c']}, 
                          {'parts_name': ['沓座モルタル Bm'], 'number': ['0101'], 'damage_name': ['⑦剥離・鉄筋露出'], 'damage_lank': ['c']}, 
                          {'parts_name': ['排水管 Dp'], 'number': ['0101'], 'damage_name': ['①腐食(大大)'], 'damage_lank': ['e']}, 
                          {'parts_name': ['排水管 Dp'], 'number': ['0101'], 'damage_name': ['⑤防食機能の劣化(分類1)'], 'damage_lank': ['e']}, 
                          {'parts_name': ['排水管 Dp'], 'number': ['0102'], 'damage_name': ['①腐食(小大)'], 'damage_lank': ['c']}, 
                          {'parts_name': ['排水管 Dp'], 'number': ['0102'], 'damage_name': ['⑤防食機能の劣化(分類1)'], 'damage_lank': ['e']}, 
                          {'parts_name': ['排水管 Dp'], 'number': ['0101'], 'damage_name': ['①腐食(大大)'], 'damage_lank': ['e']}, 
                          {'parts_name': ['排水管 Dp'], 'number': ['0101'], 'damage_name': ['⑤防食機能の劣化(分類1)'], 'damage_lank': ['e']}, 
                          {'parts_name': ['排水管 Dp'], 'number': ['0101'], 'damage_name': ['①腐食(大大)'], 'damage_lank': ['c']}, 
                          {'parts_name': ['排水管 Dp'], 'number': ['0101'], 'damage_name': ['⑤防食機能の劣化(分類1)'], 'damage_lank': ['e']}]


order_lank = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}

# 一時的な辞書を作成
temp_dict = {}

for part in split_parts_and_damage:
    key = (tuple(part['parts_name']), tuple(part['number']), tuple(part['damage_name']))
    
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
        'damage_lank': damage_lank_list
    })

# print(sorted_split)
sorted_split = [{'parts_name': ['横桁 Cr'], 'number': ['0102'], 'damage_name': ['⑰その他(分類6:施工不良)'], 'damage_lank': ['e']}, 
                {'parts_name': ['床版 Ds'], 'number': ['0201'], 'damage_name': ['⑦剥離・鉄筋露出'], 'damage_lank': ['d']}, 
                {'parts_name': ['床版 Ds'], 'number': ['0203'], 'damage_name': ['⑦剥離・鉄筋露出'], 'damage_lank': ['d']}, 
                {'parts_name': ['橋台[胸壁] Ap'], 'number': ['0101'], 'damage_name': ['⑳漏水・滞水'], 'damage_lank': ['e']}, 
                {'parts_name': ['橋台[竪壁] Ac'], 'number': ['0101'], 'damage_name': ['⑳漏水・滞水'], 'damage_lank': ['e']}, 
                {'parts_name': ['伸縮装置 Ej'], 'number': ['0101'], 'damage_name': ['⑳漏水・滞水'], 'damage_lank': ['e']}, 
                {'parts_name': ['支承本体 Bh'], 'number': ['0101'], 'damage_name': ['①腐食(小小)'], 'damage_lank': ['b']}, 
                {'parts_name': ['支承本体 Bh'], 'number': ['0101'], 'damage_name': ['⑤防食機能の劣化(分類1)'], 'damage_lank': ['e']}, 
                {'parts_name': ['支承本体 Bh'], 'number': ['0101'], 'damage_name': ['㉓変形・欠損'], 'damage_lank': ['c']}, 
                {'parts_name': ['沓座モルタル Bm'], 'number': ['0101'], 'damage_name': ['⑦剥離・鉄筋露出'], 'damage_lank': ['c']}, 
                {'parts_name': ['排水管 Dp'], 'number': ['0101'], 'damage_name': ['①腐食(大大)'], 'damage_lank': ['e']}, 
                {'parts_name': ['排水管 Dp'], 'number': ['0101'], 'damage_name': ['⑤防食機能の劣化(分類1)'], 'damage_lank': ['e']}, 
                {'parts_name': ['排水管 Dp'], 'number': ['0102'], 'damage_name': ['①腐食(小大)'], 'damage_lank': ['e']}, 
                {'parts_name': ['排水管 Dp'], 'number': ['0102'], 'damage_name': ['⑤防食機能の劣化(分類1)'], 'damage_lank': ['e']}]

number_create = [{'parts_name': ['床版 Ds'], 'number': ['0201'], 'material': ['C'], 'main_frame': ['〇']}, 
                 {'parts_name': ['排水管 Dp'], 'number': ['0102'], 'material': ['S'], 'main_frame': ['✕']}, 
                 {'parts_name': ['添架物 Ut'], 'number': ['0101'], 'material': ['S'], 'main_frame': ['✕']}]

# 結果格納用のリスト
result = []

# sorted_splitをループし、number_createと比較
for item in sorted_split:
    for nc_item in number_create:
        if item['parts_name'] == nc_item['parts_name'] and item['number'] == nc_item['number']:
            item.update({'material': nc_item['material'], 'main_frame': nc_item['main_frame']})
            break
    result.append(item)

# number_createの項目を結果に追加
for nc_item in number_create:
    # sorted_splitに存在しない場合のチェック
    exists = any(item['parts_name'] == nc_item['parts_name'] and item['number'] == nc_item['number'] for item in sorted_split)
    if not exists:
        result.append({'parts_name': nc_item['parts_name'], 'number': nc_item['number'], 'material': nc_item['material'], 'main_frame': nc_item['main_frame']})

# 指定した順番でキーを整列
ordered_result = []
ordered_keys = ['parts_name', 'number', 'material', 'damage_lank', 'damage_name', 'main_frame']

for item in result:
    ordered_item = {key: item[key] for key in ordered_keys if key in item}
    ordered_result.append(ordered_item)

# 結果の表示
#print(ordered_result)

ordered_result = [{'parts_name': ['横桁 Cr'], 'number': ['0102'], 'damage_lank': ['e'], 'damage_name': ['⑰その他(分類6:施工不良)']}, 
                  {'parts_name': ['床版 Ds'], 'number': ['0201'], 'material': ['C'], 'damage_lank': ['d'], 'damage_name': ['⑦剥離・鉄筋露出'], 'main_frame': ['〇']}, 
                  {'parts_name': ['床版 Ds'], 'number': ['0203'], 'damage_lank': ['d'], 'damage_name': ['⑦剥離・鉄筋露出']}, 
                  {'parts_name': ['橋台[胸壁] Ap'], 'number': ['0101'], 'damage_lank': ['e'], 'damage_name': ['⑳漏水・滞水']}, 
                  {'parts_name': ['橋台[竪壁] Ac'], 'number': ['0101'], 'damage_lank': ['e'], 'damage_name': ['⑳漏水・滞水']}, 
                  {'parts_name': ['伸縮装置 Ej'], 'number': ['0101'], 'damage_lank': ['e'], 'damage_name': ['⑳漏水・滞水']}, 
                  {'parts_name': ['支承本体 Bh'], 'number': ['0101'], 'damage_lank': ['b'], 'damage_name': ['①腐食(小小)']}, 
                  {'parts_name': ['支承本体 Bh'], 'number': ['0101'], 'damage_lank': ['e'], 'damage_name': ['⑤防食機能の劣化(分類1)']}, 
                  {'parts_name': ['支承本体 Bh'], 'number': ['0101'], 'damage_lank': ['c'], 'damage_name': ['㉓変形・欠損']}, 
                  {'parts_name': ['沓座モルタル Bm'], 'number': ['0101'], 'damage_lank': ['c'], 'damage_name': ['⑦剥離・鉄筋露出']}, 
                  {'parts_name': ['排水管 Dp'], 'number': ['0101'], 'damage_lank': ['e'], 'damage_name': ['①腐食(大大)']}, 
                  {'parts_name': ['排水管 Dp'], 'number': ['0101'], 'damage_lank': ['e'], 'damage_name': ['⑤防食機能の劣化(分類1)']}, 
                  {'parts_name': ['排水管 Dp'], 'number': ['0102'], 'material': ['S'], 'damage_lank': ['e'], 'damage_name': ['①腐食(小大)'], 'main_frame': ['✕']}, 
                  {'parts_name': ['排水管 Dp'], 'number': ['0102'], 'material': ['S'], 'damage_lank': ['e'], 'damage_name': ['⑤防食機能の劣化(分類1)'], 'main_frame': ['✕']}, 
                  {'parts_name': ['添架物 Ut'], 'number': ['0101'], 'material': ['S'], 'main_frame': ['✕']}]