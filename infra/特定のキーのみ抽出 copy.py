from collections import defaultdict
import re

# データ (サンプル)
sorted_items = [
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
    {'parts_name': [['橋台[胸壁] Ap0101', '橋台[竪壁] Ac0101', '伸縮装置 Ej0101']], 'damage_name': [['⑳漏水・滞水-e']], 
     'join': [{'parts_name': ['橋台[胸壁] Ap0101'], 'damage_name': ['⑳漏水・滞水-e']}, {'parts_name': ['橋台[竪壁] Ac0101'], 'damage_name': ['⑳漏水・滞水-e']}, {'parts_name': ['伸縮装置 Ej0101'], 'damage_name': ['⑳漏水・滞水-e']}], 
     'picture_number': '写真番号-18', 'this_time_picture': ['infra\img\9月7日　佐藤　地上\P9070438.JPG'], 
     'last_time_picture': 'media\P6100002.JPG', 
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
    {'parts_name': [['床版 Ds0201', '床版 Ds0203']], 'damage_name': [['⑦剥離・鉄筋露出-d']], 
     'join': [{'parts_name': ['床版 Ds0201'], 'damage_name': ['⑦剥離・鉄筋露出-d']}, {'parts_name': ['床版 Ds0203'], 'damage_name': ['⑦剥離・鉄筋露出-d']}], 
     'picture_number': None, 'this_time_picture': None, 
     'last_time_picture': None, 
     'textarea_content': '床版に鉄筋露出が見られる。 \n【関連損傷】\n床版 Ds0203:⑦剥離・鉄筋露出-d', 
     'damage_coordinate': ['525003.839727268', '213095.7270112425'], 'picture_coordinate': None}
    ,
    {'parts_name': [['排水管 Dp0103']], 'damage_name': [['①腐食(大大)-e', '⑤防食機能の劣化(分類1)-e']], 
     'join': [{'parts_name': ['排水管 Dp0101'], 'damage_name': ['①腐食(大大)-e', '⑤防食機能の劣化(分類1)-e']}], 
     'picture_number': '写真番号-31', 'this_time_picture': ['infra\img\9月7日　佐藤　地上\P9070422.JPG'], 
     'last_time_picture': None, 
     'textarea_content': '排水管に板厚減少を伴う拡がりのある腐食,点錆が見られる。\n【関連損傷】\n排水管 Dp0101:⑤防食機能の劣化(分類1)-e', 
     'damage_coordinate': ['538482.3557216563', '229268.8593029478'], 'picture_coordinate': ['538810.3087944178', '228910.3502713814']}
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
    {'parts_name': [['床版 Ds0201', '床版 Ds0203']], 'damage_name': [['⑦剥離・鉄筋露出-d']], 
     'join': [{'parts_name': ['床版 Ds0201'], 'damage_name': ['⑦剥離・鉄筋露出-d']}, {'parts_name': ['床版 Ds0203'], 'damage_name': ['⑦剥離・鉄筋露出-d']}], 
     'picture_number': None, 'this_time_picture': None, 
     'last_time_picture': None, 
     'textarea_content': '床版に鉄筋露出が見られる。 \n【関連損傷】\n床版 Ds0203:⑦剥離・鉄筋露出-d', 
     'damage_coordinate': ['525003.839727268', '213095.7270112425'], 'picture_coordinate': None}
    ,
    {'parts_name': [['排水管 Dp0103']], 'damage_name': [['①腐食(大大)-e', '⑤防食機能の劣化(分類1)-e']], 
     'join': [{'parts_name': ['排水管 Dp0101'], 'damage_name': ['①腐食(大大)-e', '⑤防食機能の劣化(分類1)-e']}], 
     'picture_number': '写真番号-31', 'this_time_picture': ['infra\img\9月7日　佐藤　地上\P9070422.JPG'], 
     'last_time_picture': None, 
     'textarea_content': '排水管に板厚減少を伴う拡がりのある腐食,点錆が見られる。\n【関連損傷】\n排水管 Dp0101:⑤防食機能の劣化(分類1)-e', 
     'damage_coordinate': ['538482.3557216563', '229268.8593029478'], 'picture_coordinate': ['538810.3087944178', '228910.3502713814']}
    ,
    {'parts_name': [['PC定着部 Cn1102']], 'damage_name': [['NON-a']], 
     'join': [{'parts_name': ['PC定着部 Cn1102'], 'damage_name': ['NON-a']}], 
     'picture_number': '写真番号-4,5', 'this_time_picture': None, 
     'last_time_picture': None, 
     'textarea_content': '横桁に施工不良が見られる。', 
     'damage_coordinate': ['532578.7587482664', '229268.8593029478'], 'picture_coordinate': ['532985.6409545547', '228954.2335446222']}
]

result_items = []

for item in sorted_items:
    join_items = item.get('join', [])
    pictures = item.get('this_time_picture', [])
    
    # 各 join 要素に picture を追加
    for join_item in join_items:
        join_item['this_time_picture'] = pictures
    
    result_items.append({'join': join_items})

# joinキーのみを抽出
join_values = [item['join'] for item in result_items]

# join値を1行にまとめる
flattened_join = [join_item for sublist in join_values for join_item in sublist]

order_number = {"None": 0, "①": 1, "②": 2, "③": 3, "④": 4, "⑤": 5, "⑥": 6, "⑦": 7, "⑧": 8, "⑨": 9, "⑩": 10, "⑪": 11, "⑫": 12, "⑬": 13, "⑭": 14, "⑮": 15, "⑯": 16, "⑰": 17, "⑱": 18, "⑲": 19, "⑳": 20, "㉑": 21, "㉒": 22, "㉓": 23, "㉔": 24, "㉕": 25, "㉖": 26}
order_lank = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}

main_parts_list_left = ["PC定着部"] # 左の数字
main_parts_list_right = ["横桁", "橋台"] # 右の数字
main_parts_list_zero = ["床版"] # 00になる場合

# データをグループ化するための辞書
grouped_data = defaultdict(lambda: defaultdict(lambda: {'lanks': [], 'pictures': []}))

for item in flattened_join:
    #print(f"item:{item}")
    name_and_number = item['parts_name'][0]
    
    if any(word in name_and_number for word in main_parts_list_left):
        left = name_and_number.find(" ")
        title2 = name_and_number[:left]
        number2 = name_and_number[left+1:]
        number_part = re.search(r'[A-Za-z]*(\d+)', number2).group(1)
        parts_name = name_and_number[:left]+" "+number_part[:2] # 主桁 03
    elif any(word in name_and_number for word in main_parts_list_right):
        right = name_and_number.find(" ")
        title2 = name_and_number[:right]
        number2 = name_and_number[right+1:]
        number_part = re.search(r'[A-Za-z]*(\d+)', number2).group(1)
        if len(number_part) < 5:
            parts_name = name_and_number[:right]+" "+number_part[2:] # 横桁 02
        else:
            parts_name = name_and_number[:right]+" "+number_part[2:] # 横桁 103
    elif any(word in name_and_number for word in main_parts_list_zero):
        right = name_and_number.find(" ")
        parts_name = name_and_number[:right]+" 00"
    else:
        right = name_and_number.find(" ")
        parts_name = name_and_number[:right]

    for damage in item['damage_name']:
        damage_split = damage.rsplit('-', 1)
        
        if damage_split[0].startswith(('⑰')):# 他にもあれば、('㉓', '㉔')と記入
          damage_name = damage_split[0][1:]
        else:
          sub_damage_name = damage_split[0]
          
          # 最初のカッコの位置を探す
          first_parenthesis_index = sub_damage_name.find('(')

          # カッコの位置より前を抽出する
          if first_parenthesis_index != -1:  # カッコが見つかった場合
              damage_name = sub_damage_name[:first_parenthesis_index][1:]
          elif sub_damage_name == "NON":
              damage_name = sub_damage_name
          else:  # カッコが見つからない場合
              damage_name = sub_damage_name[1:]

        damage_lank = damage_split[1]
        grouped_data[parts_name][damage_name].append(damage_lank)
           
    picture = item['this_time_picture']

# 重複削除と並び替えを行う関数
def unique_sorted_lanks(lanks, order_lank):
    unique_lanks = list(sorted(set(lanks), key=lambda x: order_lank[x]))
    return unique_lanks

# 新しいリストを作成
change_list = [
    {'parts_name': [parts], 'damage_name': [damage], 'damage_lank': unique_sorted_lanks(lanks, order_lank), 'this_time_picture': [picture]}
    for parts, damages in grouped_data.items()
    for damage, lanks in damages.items()
]

# 結果の表示
print(change_list)