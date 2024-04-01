order_dict = {"主桁": 1, "横桁": 2, "床版": 3, "PC定着部": 4, "防護柵": 5, "伸縮装置": 6}
#優先順位の指定

text_list = [['PC定着部 Cn1203', '①-d'],['主桁 Mg0901', '①-c'],['PC定着部 Cn1104'],['主桁 Mg0401', '⑨'],['床版 Ds0201', '⑪-d'],['主桁,伸縮装置 Mg0101,Ej0201', '①-d'],['床版 Ds0201', '⑧-d']]
#入力したデータ

def sort_category(text): # sort_category関数を定義
     for key, val in order_dict.items(): # keyがキー(主桁～防護柵)、valが値(1～6)
       #print(key , val)
         if text.startswith(key): # textの1文字目がキー(主桁～防護柵)の場合
             return val # 値(1～6)を返す
     return len(order_dict) # order_dictの要素の数を返す

orted_text_list = sorted(text_list, key=lambda text: (sort_category(text[0]), text[0]))
# sorted(並び替えるオブジェクト, lamda式(無名関数)で並び替え 各要素: (text[0]で始まる要素を並び替え、その中でtext[0]の並び替え))

print(orted_text_list)
#[['主桁 Mg0901'], ['床版 Ds0201'], ['PC定着部 Cn1203'], ['PC定着部 Cn1424']]

