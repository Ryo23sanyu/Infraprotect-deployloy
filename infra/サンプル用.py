import re


data = [
    {'first': [['排水管 Dp0101']], 'second': [['①腐食(大大)-e', '⑤防食機能の劣化(分類1)-e']], 
     'join': [{'first': ['排水管 Dp0101'], 'second': ['①腐食(大大)-e', '⑤防食機能の劣化(分類1)-e']}], 
     'third': '写真番号-31', 'last': ['C:\\work\\django\\myproject\\program\\Infraproject\\infra\\static\\infra\\img\\9月7日　佐藤　地上\\P9070422.JPG'], 
     'picture': None, 
     'textarea_content': '排水管に板厚減少を伴う拡がりのある腐食,点錆が見られる。\n【関連損傷】\n排水管 Dp0101:⑤防食機能の劣化(分類1)-e', 
     'damage_coordinate': ['538482.3557216563', '229268.8593029478'], 'picture_coordinate': ['538810.3087944178', '228910.3502713814']}
     ,
    {'first': [['排水管 Dp0101']], 'second': [['①腐食(小大)-c', '⑤防食機能の劣化(分類1)-e', '㉓変形・欠損-c']], 
     'join': [{'first': ['排水管 Dp0101'], 'second': ['①腐食(小大)-c', '⑤防食機能の劣化(分類1)-e', '㉓変形・欠損-c']}], 
     'third': '写真番号-32', 'last': ['C:\\work\\django\\myproject\\program\\Infraproject\\infra\\static\\infra\\img\\9月7日　佐藤　地上\\P9070486.JPG'], 
     'picture': None, 
     'textarea_content': '排水管に拡がりのある腐食,点錆が見られる。\n【関連損傷】\n排水管 Dp0102:⑤防食機能の劣化(分類1)-e', 
     'damage_coordinate': ['547059.1990495767', '229268.8593029478'], 'picture_coordinate': ['549204.9604817769', '229256.3408485695']}
    ,
    {'first': [['橋台[胸壁] Ap0101', '橋台[竪壁] Ac0101', '伸縮装置 Ej0101']], 'second': [['⑳漏水・滞水-e']], 
     'join': [{'first': ['橋台[胸壁] Ap0101'], 'second': ['⑳漏水・滞水-e']}, {'first': ['橋台[竪壁] Ac0101'], 'second': ['⑳漏水・滞水-e']}, {'first': ['伸縮装置 Ej0101'], 'second': ['⑳漏水・滞水-e']}], 
     'third': '写真番号-18', 'last': ['C:\\work\\django\\myproject\\program\\Infraproject\\infra\\static\\infra\\img\\9月7日　佐藤　地上\\P9070438.JPG'], 
     'picture': 'C:\\work\\django\\myproject\\program\\Infraproject\\media\\P6100002.JPG', 
     'textarea_content': '橋台[胸壁]および橋台[竪壁],伸縮装置に漏水・滞水が見られる。 \n【関連損傷】\n橋台[竪壁] Ac0101,伸縮装置 Ej0101:⑳漏水・滞水-e', 
     'damage_coordinate': ['535305.6406762057', '190342.4721676922'], 'picture_coordinate': ['537494.8440878117', '190371.7813098583']}
    ,
    {'first': [['床版 Ds0201', '床版 Ds0203']], 'second': [['⑦剥離・鉄筋露出-d']], 
     'join': [{'first': ['床版 Ds0201'], 'second': ['⑦剥離・鉄筋露出-d']}, {'first': ['床版 Ds0203'], 'second': ['⑦剥離・鉄筋露出-d']}], 
     'third': None, 'last': None, 
     'picture': None, 
     'textarea_content': '床版に鉄筋露出が見られる。 \n【関連損傷】\n床版 Ds0203:⑦剥離・鉄筋露出-d', 
     'damage_coordinate': ['525003.839727268', '213095.7270112425'], 'picture_coordinate': None}
]


combined_results = {}

# joinキーのみ取り出す
for item in data:
    for join in item['join']:
        first_key = tuple(join['first'])
        second_values = join['second']
        
        if first_key not in combined_results:
            combined_results[first_key] = set()
        
        combined_results[first_key].update(second_values)

# Convert the combined dictionary back into the desired list format
result = []
for first_key, second_values in combined_results.items():
    new_item = {'join': [{'first': list(first_key), 'second': list(second_values)}]}
    result.append(new_item)

# Print the resulting data
print(result)