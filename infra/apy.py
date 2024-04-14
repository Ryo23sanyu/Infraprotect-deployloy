order_dict = {"主桁": 1, "横桁": 2, "床版": 3, "PC定着部": 4, "防護柵": 5}
order_number = {"None": 0, "①": 1, "②": 2, "③": 3, "④": 4, "⑤": 5, "⑥": 6, "⑦": 7, "⑧": 8, "⑨": 9, "⑩": 10, "⑪": 11, "⑫": 12, "⑬": 13, "⑭": 14, "⑮": 15, "⑯": 16, "⑰": 17, "⑱": 18, "⑲": 19, "⑳": 20, "㉑": 21, "㉒": 22, "㉓": 23, "㉔": 24, "㉕": 25, "㉖": 26}
#優先順位の指定

text_list = {"first": 'PC定着部 Cn1103', "second": 'None'},{"first": 'PC定着部 Cn1203', "second": '⑤-d'},{"first": '主桁 Mg0901', "second": '⑥-d'},\
    {"first": 'PC定着部 Cn1424', "second": '①-d'},{"first": '主桁 Mg0401', "second": '⑦-d'},{"first": 'PC定着部 Cn1203', "second": '③-d'}
    
def sort_category(text):
     for key, val in order_dict.items():
         if text.startswith(key):
             return val
     return len(order_dict)
    
def sort_number(second_text):
    num_text = second_text.split('-')[0]  # 例えば "①-d" の "①" の部分を取得
    for key, val in order_number.items():
        if key == num_text:
            return val
    return len(order_number)

damage_table = []

damage_table.append(text_list)
 
sorted_text_list = sorted(damage_table, key=lambda text: (sort_category(text['first']), text['first'], sort_number(text['second'])))

print(damage_table)
# [{'first': '主桁 Mg0401', 'second': '⑦-d'}, {'first': '主桁 Mg0901', 'second': '⑥-d'}, {'first': 'PC定着部 Cn1103', 'second': 'None'}, {'first': 'PC定着部 Cn1203', 'second': '③-d'}, {'first': 'PC定着部 Cn1203', 'second': '⑤-d'}, {'first': 'PC定着部 Cn1424', 'second': '①-d'}]