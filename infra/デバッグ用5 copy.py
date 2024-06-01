import re


items = [{'first': [['PC定着部 Cr0803']], 'second': [['⑦剥離・鉄筋露出-d']], 'join': [{'first': ['横桁 Cr0803'], 'second': ['⑦剥離・鉄筋露出-d']}], 'third': '写真番号-15', 'last': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070458.JPG'], 'picture': 'infra/noImage.png', 'textarea_content': '横桁に鉄筋露出が見られる。', 'damage_coordinate': ['543207.0862507953', '218366.5575399188'], 'picture_coordinate': ['545418.5774821687', '218368.3759352968']}, {'first': [['主桁 Mg0901']], 'second': [['⑰その他(分類6:異物混入)-e']], 'join': [{'first': ['主桁 Mg0901'], 'second': ['⑰その他(分類6:異物混入)-e']}], 'third': '写真番号-2', 'last': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070404.JPG'], 'picture': 'infra/noImage.png', 'textarea_content': '主桁に異物混入が見られる。', 'damage_coordinate': ['532240.3861927793', '218366.5575399188'], 'picture_coordinate': ['534192.8564975171', '218396.3930096343']}]

#優先順位の指定
order_dict = {"主桁": 1, "横桁": 2, "床版": 3, "PC定着部": 4, "橋台[胸壁]": 5, "橋台[竪壁]": 6, "支承本体": 7, "沓座モルタル": 8, "防護柵": 9, "地覆": 10, "伸縮装置": 11, "舗装": 12, "排水ます": 13, "排水管": 14}
order_number = {"None": 0, "①": 1, "②": 2, "③": 3, "④": 4, "⑤": 5, "⑥": 6, "⑦": 7, "⑧": 8, "⑨": 9, "⑩": 10, "⑪": 11, "⑫": 12, "⑬": 13, "⑭": 14, "⑮": 15, "⑯": 16, "⑰": 17, "⑱": 18, "⑲": 19, "⑳": 20, "㉑": 21, "㉒": 22, "㉓": 23, "㉔": 24, "㉕": 25, "㉖": 26}
order_lank = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
        
# <<◆ リストの並び替え ◆>>
def sort_key_function(sort_item):
    first_value = sort_item['first'][0][0] # firstキーの最初の要素
    #print(first_value) # 主桁 Mg0901

    if " " in first_value:
        # 部材記号の前にスペースが「含まれている」場合
        first_value_split = first_value.split()
        #print(first_value_split) # ['主桁', 'Mg0901']
    else:
        # 部材記号の前にスペースが「含まれていない」場合
        first_value_split = re.split(r'(?<=[^a-zA-Z])(?=[a-zA-Z])', first_value) # アルファベット以外とアルファベットの並びで分割
        first_value_split = [x for x in first_value_split if x] # re.split()の結果には空文字が含まれるので、それを取り除く
        #print(first_value_split) # ['主桁', 'Mg0901']

    first_name_key = order_dict.get(first_value_split[0], 0)
    #print(first_name_key) # 1

    first_number_key = int(first_value_split[1][2:])
    #print(first_number_key) # 901

    if sort_item['second'][0][0]:  # `second`キーが存在する場合
        second_value = sort_item['second'][0][0] # secondキーの最初の要素
        #print(second_value) # ⑰その他(分類6:異物混入)-e
        second_number_key = order_number.get(second_value[0], 0)  # 先頭の文字を取得してorder_numberに照らし合わせる
        #print(second_number_key) # 17
        second_lank_key = order_lank.get(second_value[-1], 0)  # 末尾の文字を取得してorder_lankに照らし合わせる
        #print(second_lank_key) # 5
    else:
        second_key = 0
        second_lank = 0
            
    return (first_name_key, first_number_key, second_number_key, second_lank_key)

sorted_items = sorted(items, key=sort_key_function)

# ソート結果を表示
for item in sorted_items:
    print(item)