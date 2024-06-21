import re

result = [{'join': [{'first': ['排水管 Dp0101'], 'second': ['㉓変形・欠損-c', '①腐食(小大)-c', '①腐食(大大)-e', '⑤防食機能の劣化(分類1)-e']}]}, 
          {'join': [{'first': ['橋台[胸壁] Ap0101'], 'second': ['⑳漏水・滞水-e']}]}, {'join': [{'first': ['橋台[竪壁] Ac0101'], 'second': ['⑳漏水・滞水-e']}]}, {'join': [{'first': ['伸縮装置 Ej0101'], 'second': ['⑳漏水・滞水-e']}]}, 
          {'join': [{'first': ['床版 Ds0201'], 'second': ['⑦剥離・鉄筋露出-d']}]}, {'join': [{'first': ['床版 Ds0203'], 'second': ['⑦剥離・鉄筋露出-d']}]}]


#優先順位の指定
order_dict = {"主桁": 1, "横桁": 2, "床版": 3, "PC定着部": 4, "橋台[胸壁]": 5, "橋台[竪壁]": 6, "支承本体": 7, "沓座モルタル": 8, "防護柵": 9, "地覆": 10, "伸縮装置": 11, "舗装": 12, "排水ます": 13, "排水管": 14}
order_number = {"None": 0, "①": 1, "②": 2, "③": 3, "④": 4, "⑤": 5, "⑥": 6, "⑦": 7, "⑧": 8, "⑨": 9, "⑩": 10, "⑪": 11, "⑫": 12, "⑬": 13, "⑭": 14, "⑮": 15, "⑯": 16, "⑰": 17, "⑱": 18, "⑲": 19, "⑳": 20, "㉑": 21, "㉒": 22, "㉓": 23, "㉔": 24, "㉕": 25, "㉖": 26}
order_lank = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}

# <<◆ リストの並び替え ◆>>
def sort_key_function(item):
    first_value = item['join'][0]['first'][0]
    #print(first_value) # 排水管 Dp0101

    if " " in first_value:
        first_name, first_code = first_value.split()
        #print(first_name) # 排水管
        #print(first_code) # Dp0101

    first_name_key = order_dict.get(first_name, float('inf'))
    #print(first_name_key) # 排水管をorder_dictの番号に変更 # 14

    match = re.search(r'[A-Za-z]+(\d{2,})(\D)?', first_code) # アルファベット+2文字以上の数字+数字以外が0回もしくは1回
    if match:
        first_number_key = int(match.group(1))
        #print(first_number_key) # 101

    second_list = item['join'][0]['second']
    #print(second_list) # ['㉓変形・欠損-c', '①腐食(小大)-c', '①腐食(大大)-e', '⑤防食機能の劣化(分類1)-e']
    
    second_values = []
    for second_value in second_list:
        match = re.match(r"([①-⑳㉑-㉖])[^-]*-([a-e])", second_value)
        number, lank = match.groups() #①～㉖ # a-e
        second_number_key = order_number.get(number, float('inf')) # 1～26
        second_lank_key = order_lank.get(lank, float('inf')) # 1～5(a:1、e:5)

        second_values.append((second_number_key, second_lank_key, second_value))
    #print(second_values) # [(23, 3, '㉓変形・欠損-c'), (1, 3, '①腐食(小大)-c'), (1, 5, '①腐食(大大)-e'), (5, 5, '⑤防食機能の劣化(分類1)-e')]
    if second_values:
        second_values = sorted(second_values)
        print(second_values) # [(1, 3, '①腐食(小大)-c'), (1, 5, '①腐食(大大)-e'), (5, 5, '⑤防食機能の劣化(分類1)-e'), (23, 3, '㉓変形・欠損-c')]
        second_values_sorted = [val[2] for val in second_values]
        print(second_values_sorted) # ['①腐食(小大)-c', '①腐食(大大)-e', '⑤防食機能の劣化(分類1)-e', '㉓変形・欠損-c']
    else:
        second_number_key, second_lank_key = float('inf'), float('inf')
        second_values_sorted = []

    item['join'][0]['second'] = second_values_sorted
    return (first_name_key, first_number_key, second_values[0][0], second_values[0][1])

sorted_items = sorted(result, key=sort_key_function)
print("Sorted items:")
print(sorted_items)

