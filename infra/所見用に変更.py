from collections import defaultdict
import re

flattened_join = [
    {'parts_name': ['排水管 Dp0101'], 'damage_name': ['①腐食(大大)-e', '⑤防食機能の劣化(分類1)-e']},
    {'parts_name': ['排水管 Dp0101'], 'damage_name': ['③ゆるみ・脱落-e']}, 
    {'parts_name': ['排水管 Dp0102'], 'damage_name': ['①腐食(小大)-c', '⑤防食機能の劣化(分類1)-e']}, 
    {'parts_name': ['添架物 Ut0101'], 'damage_name': ['③ゆるみ・脱落-e']}
    ]

order_number = {"None": 0, "①": 1, "②": 2, "③": 3, "④": 4, "⑤": 5, "⑥": 6, "⑦": 7, "⑧": 8, "⑨": 9, "⑩": 10, "⑪": 11, "⑫": 12, "⑬": 13, "⑭": 14, "⑮": 15, "⑯": 16, "⑰": 17, "⑱": 18, "⑲": 19, "⑳": 20, "㉑": 21, "㉒": 22, "㉓": 23, "㉔": 24, "㉕": 25, "㉖": 26}
order_lank = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}

main_parts_list_left = ["主桁"] # 左の数字
main_parts_list_right = ["横桁"] # 右の数字
main_parts_list_zero = ["床版"] # 00になる場合

# データをグループ化するための辞書
grouped_data = defaultdict(lambda: defaultdict(list))

for item in flattened_join:
    name_and_number = item['parts_name'][0]
    if name_and_number in main_parts_list_left:
        right = name_and_number.find(" ")
        right = name_and_number.find(" ")
        title2 = name_and_number[:right]
        number2 = name_and_number[right+1:]
        number_part = re.search(r'[A-Za-z]*(\d+)', number2).group(1)
        parts_name = name_and_number[:right]+" "+number_part[:2] # 主桁 03
    elif name_and_number in main_parts_list_right:
        right = name_and_number.find(" ")
        title2 = name_and_number[:right]
        number2 = name_and_number[right+1:]
        number_part = re.search(r'[A-Za-z]*(\d+)', number2).group(1)
        if len(number_part) < 5:
            parts_name = name_and_number[:right]+" "+number_part[2:] # 横桁 02
        else:
            parts_name = name_and_number[:right]+" "+number_part[2:] # 横桁 103
    elif name_and_number in main_parts_list_zero:
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
          else:  # カッコが見つからない場合
              damage_name = sub_damage_name[1:]

        damage_lank = damage_split[1]
        grouped_data[parts_name][damage_name].append(damage_lank)

# 重複削除と並び替えを行う関数
def unique_sorted_lanks(lanks, order_lank):
    unique_lanks = list(sorted(set(lanks), key=lambda x: order_lank[x]))
    return unique_lanks

# 新しいリストを作成
change_list = [
    {'parts_name': [parts], 'damage_name': [damage], 'damage_lank': unique_sorted_lanks(lanks, order_lank)}
    for parts, damages in grouped_data.items()
    for damage, lanks in damages.items()
]

# 結果の表示
print(change_list)