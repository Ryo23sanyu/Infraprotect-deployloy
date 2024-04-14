order_dict = {"主桁": 1, "横桁": 2, "床版": 3, "PC定着部": 4, "橋台[胸壁]": 5, "橋台[竪壁]": 6, "支承本体": 7, "沓座モルタル": 8, "防護柵": 9, "地覆": 10, "伸縮装置": 11, "舗装": 12, "排水ます": 13, "排水管": 14}
order_number = {"None": 0, "①": 1, "②": 2, "③": 3, "④": 4, "⑤": 5, "⑥": 6, "⑦": 7, "⑧": 8, "⑨": 9, "⑩": 10, "⑪": 11, "⑫": 12, "⑬": 13, "⑭": 14, "⑮": 15, "⑯": 16, "⑰": 17, "⑱": 18, "⑲": 19, "⑳": 20, "㉑": 21, "㉒": 22, "㉓": 23, "㉔": 24, "㉕": 25, "㉖": 26}
order_lank = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
#優先順位の指定

text_list = [{'first': 'PC定着部 Cn1203','second': ['①腐食(大小)-d']},{'first': '主桁 Mg0901','second': ['①腐食(小大)-c']},{'first': 'PC定着部 Cn1104','second': ['']},\
    {'first': '主桁 Mg0401','second': ['⑨抜け落ち-e']},{'first': 'PC定着部 Cn1203','second': ['①腐食(小小)-b']},{'first': '床版 Ds0201','second': ['⑪床版ひびわれ-d']},\
        {'first': '主桁,伸縮装置 Mg0101,Ej0201','second': ['①腐食(大小)-d']},{'first': '床版 Ds0201','second': ['⑧漏水・遊離石灰-d']},\
            {'first': '主桁 Mg0901','second': ['⑰その他(分類6:異物混入)-e']},{'first': '主桁 Mg0901','second': ['⑦剥離・鉄筋露出-c']},\
                {'first': '舗装 Pm0101','second': ['㉔土砂詰まり-e']},{'first': '舗装 Pm0101,0201','second': ['⑮舗装の異常-e']},\
                    {'first': '舗装 Pm0201','second': ['⑮舗装の異常-e']}]
#入力したデータ

def sort_category(text): # sort_category関数を定義
     for key, val in order_dict.items(): # keyがキー(主桁～防護柵)、valが値(1～6)
         if text.startswith(key): # textの1文字目がキー(主桁～防護柵)の場合
             return val # 値(1～6)を返す
     return max(order_dict.values()) + 1

def extract_numbers(s):
    # 文字列から数値部分だけを抽出してリストに格納する
    return [int(''.join(filter(str.isdigit, part))) for part in s.split(',') if ''.join(filter(str.isdigit, part))]

def get_first_key(first):
    num_parts = extract_numbers(first)
    # 数値が含まれていない場合は、ソートで最後になるような大きな値を返す
    return min(num_parts) if num_parts else float('inf')

def sort_number(second_list):
    # リストが空の場合の処理
    if not second_list or len(second_list) == 0:  # 条件式の調整
        return max(order_number.values()) + 1
    else:
        second_text = second_list[0]
        if "-" in second_text: #second_textの文字の中に-があるとき
            num_text = second_text[0] #num_textにsecond_textの1文字目を入れる
            for key, val in order_number.items():
                if num_text.startswith(key):
                    return val #数字を返す
    return max(order_number.values()) + 1 #リストの最大数+1の数字を返す

def sort_lank(second_list):
    if not second_list or len(second_list) == 0:  # 条件式の調整
        return max(order_number.values()) + 1
    else:
        second_text = second_list[0]
        if '-' in second_text:
            lank_text = second_text.split("-")[1]
            for key, val in order_lank.items():
                if lank_text.startswith(key):
                    return val
        return max(order_lank.values()) + 1
 
sorted_text_list = sorted(text_list, key=lambda text: (sort_category(text['first']), get_first_key(text['first']), sort_number(text['second']), sort_lank(text['second'])))

print(sorted_text_list)