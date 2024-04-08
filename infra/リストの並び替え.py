order_dict = {"主桁": 1, "横桁": 2, "床版": 3, "PC定着部": 4, "橋台[胸壁]": 5, "橋台[竪壁]": 6, "支承本体": 7, "沓座モルタル": 8, "防護柵": 9, "地覆": 10, "伸縮装置": 11, "舗装": 12, "排水ます": 13, "排水管": 14}
#優先順位の指定
order_number = {"①": 1, "②": 2, "③": 3, "④": 4, "⑤": 5, "⑥": 6, "⑦": 7, "⑧": 8, "⑨": 9, "⑩": 10, "⑪": 11, "⑫": 12, "⑬": 13, "⑭": 14, "⑮": 15, "⑯": 16, "⑰": 17, "⑱": 18, "⑲": 19, "⑳": 20, "㉑": 21, "㉒": 22, "㉓": 23, "㉔": 24, "㉕": 25, "㉖": 26}
#優先順位の指定

text_list = [['PC定着部 Cn1203', '①-d'],['主桁 Mg0901', '①-c'],['PC定着部 Cn1104'],['主桁 Mg0401', '⑨'],['床版 Ds0201', '⑪-d'],['主桁,伸縮装置 Mg0101,Ej0201', '①-d'],['床版 Ds0201', '⑧-d']]
#入力したデータ

def sort_category(text): # sort_category関数を定義
     for key, val in order_dict.items(): # keyがキー(主桁～防護柵)、valが値(1～6)
         if text.startswith(key): # textの1文字目がキー(主桁～防護柵)の場合
             return val # 値(1～6)を返す
     return len(order_dict) # startswitchに全くマッチしなかった場合に実行(len(order_dict):6 → 順序はリストの末尾)
   
def sort_number(text):
     if len(text) > 1:  # 項目が2番目の要素も持つ場合
        num_text = text[1].split('-')[0]  # 例えば "①-d" の "①" の部分を取得
        for key, val in order_number.items():
            if num_text.startswith(key):
                return val
     return len(order_number)

orted_text_list = sorted(text_list, key=lambda text: (sort_category(text[0]), text[0], sort_number(text)))
# sorted(並び替えるオブジェクト, lamda式(無名関数)で並び替え 各要素: (text[0]で始まる要素を並び替え、その中でtext[0]の並び替え))

print(orted_text_list)
#[['主桁 Mg0901'], ['床版 Ds0201'], ['PC定着部 Cn1203'], ['PC定着部 Cn1424']]
