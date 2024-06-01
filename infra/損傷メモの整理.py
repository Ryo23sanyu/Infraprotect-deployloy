import re


replacement_patterns = {
    "①腐食(小小)-b": "腐食", # 1
    "①腐食(小大)-c": "拡がりのある腐食",
    "⑤防食機能の劣化(分類1)-e": "点錆", # 5
    "⑦剥離・鉄筋露出-c": "剥離", # 7
    "⑦剥離・鉄筋露出-d": "鉄筋露出",
}

def describe_damage(damage_list):
    described_list = []
    for damage in damage_list:
        if damage in replacement_patterns:
            described_list.append(replacement_patterns[damage])
        elif damage.startswith('⑰'):
            match = re.search(r'(?<=:)(.*?)(?=\)-e)', damage)
            if match:
                described_list.append(match.group(1))
        else:
            pattern = r'[\u3248-\u3257](.*?)-'
            match = re.search(pattern, damage)
            if match:
                described_list.append(match.group(1))
            else:
                described_list.append(damage)  # フォールバックとしてそのまま返す
    return ','.join(described_list)
  
# 各ケースに対して出力を確認:
item = {'first': [['横桁 Cr0803']], 'second': [['⑦剥離・鉄筋露出-d']]}

item = {'first': [['床版 Ds0201', '床版 Ds0203']], 'second': [['⑦剥離・鉄筋露出-d']]}

item = {'first': [['横桁 Cr0503']], 'second': [['⑦剥離・鉄筋露出-d', '⑰その他(分類6:施工不良)-e']]}

item = {'first': [['排水管 Dp0101', '排水管 Dp0102']], 'second': [['①腐食(小大)-c', '⑤防食機能の劣化(分類1)-e']]}

item = {'first': [['主桁 Mg0101', '横桁 Cr0102', '対傾構 Cf0102']], 'second': [['①腐食(小大)-c', '⑤防食機能の劣化(分類1)-e']]}

item = {'first': [['支承本体 Bh0101'], ['沓座モルタル Bm0101']], 'second': [['①腐食(小小)-b', '⑤防食機能の劣化(分類1)-e'], ['⑦剥離・鉄筋露出-c']]}

def generate_report(item):
    primary_damages = []
    processed_related_damages = []

    first_items = item['first']
    #print(first_items) # [['支承本体 Bh0101'], ['沓座モルタル Bm0101']]
    second_items = item['second']
    #print(second_items) # [['①腐食(小小)-b', '⑤防食機能の劣化(分類1)-e'], ['⑦剥離・鉄筋露出-c']]
    primary_damages_dict = {}

    for first_item, second_item in zip(first_items, second_items):
        element_names = [f.split()[0] for f in first_item] # カッコ内の要素について、スペースより前を抽出
        #print(element_names) # ['支承本体'], ['沓座モルタル']
        damage_descriptions = describe_damage(second_item) # 辞書で置換
        #print(damage_descriptions) # 腐食,点錆, 剥離
        
        if len(element_names) == 1: # ['主桁', '横桁', '対傾構']：これはだめ
            primary_damages.append(f"{element_names[0]}に{damage_descriptions}が見られる。")
            #print(primary_damages) # ['支承本体に腐食,点錆が見られる。', '沓座モルタルに剥離が見られる。']
        else:
            element_names = list(dict.fromkeys(element_names))            
            joined_elements = "および".join(element_names[:-1]) + "," + element_names[-1]
            if joined_elements.startswith(","):
                new_joined_elements = joined_elements[1:]
            else:
                new_joined_elements = joined_elements
            primary_damages.append(f"{new_joined_elements}に{damage_descriptions}が見られる。")

        for elem in first_item:
            primary_damages_dict[elem] = second_item[:]

    primary_description = "また".join(primary_damages)
        
    for elem_name, elem_number in zip(first_items, second_items): # 主桁 Mg0101
        print(f"{first_items}-{elem_name}")
        print(f"{second_items}-{elem_number}")
        print(" ")
        # リストをフラットにする関数
        def flatten_list(nested_list):
            return [item for sublist in nested_list for item in sublist]
        # フラットにしたリストを比較
        if flatten_list(first_items) != elem_name and flatten_list(second_items) != elem_number:
            sub_related_damages = []
            for first_item in first_items:
                for elem in first_item:
                    if elem in primary_damages_dict:
                        formatted_damages = ",".join(list(dict.fromkeys(primary_damages_dict[elem])))
                        sub_related_damages.append(f"{elem}:{formatted_damages}")
                        #print(related_damages) # ['支承本体 Bh0101:①腐食(小小)-b,⑤防食機能の劣化(分類1)-e', '沓座モルタル Bm0101:⑦剥離・鉄筋露出-c']

            # 処理後のリストを格納するための新しいリスト
            second_related_damages = []

            # リスト内の各要素をループする
            for i, damage in enumerate(sub_related_damages):
                # 1番目の要素の場合のみコンマのチェックを行う
                if i == 0:
                    if ',' not in damage:
                        continue  # コンマがない場合、この要素をスキップ
                # "："以降の部分を取り出す
                colon_index = damage.find(":")
                if colon_index != -1:
                    # カンマを使って分割
                    parts = damage.split(',')

                    if len(parts) > 1:
                        # 最初の部分を取り除き、残りを再結合
                        first_damage = parts[0].split(':')[0]
                        after_damage = ':' + parts[1].strip()
                        damage = first_damage + after_damage

                        if damage.endswith(":"):
                            damage = None
                
                # 処理後の要素を新しいリストに追加
                if damage:
                    second_related_damages.append(damage)

            # 処理後のリストを格納するための新しいリスト
            processed_related_damages = []
            for damage in second_related_damages:
                colon_index = damage.find(":")
                if colon_index != -1:
                    before_colon_part = damage[:colon_index].strip()
                    after_colon_part = damage[colon_index + 1:].strip()
                    if before_colon_part and after_colon_part:
                        processed_damage = f"{before_colon_part}:{after_colon_part}"
                        processed_related_damages.append(processed_damage)
            
        elif len(elem_name) < 2 and len(elem_number) < 2: # {'first': [['横桁 Cr0803']], 'second': [['⑦剥離・鉄筋露出-d']]}
            None
        elif len(elem_name) > 1 and len(elem_number) < 2: # {'first': [['床版 Ds0201', '床版 Ds0203']], 'second': [['⑦剥離・鉄筋露出-d']]}
            #print(first_item) # ['床版 Ds0201', '床版 Ds0203']
            #print(second_item) # ['⑦剥離・鉄筋露出-d']
            related_damage_list = ','.join(second_item)
            processed_related_damages.append(f"{elem_name[1]}:{related_damage_list}")
            #print(related_damages)
        elif len(elem_name) < 2 and len(elem_number) > 1: # {'first': [['横桁 Cr0503']], 'second': [['⑦剥離・鉄筋露出-d', '⑰その他(分類6:施工不良)-e']]}
            #print(first_item) # ['横桁 Cr0503']
            #print(second_item) # ['⑦剥離・鉄筋露出-d', '⑰その他(分類6:施工不良)-e']
            related_damage_list = ','.join(second_item[1:])
            #print(related_damage_list)
            processed_related_damages.append(f"{','.join(elem_name)}:{related_damage_list}")
            #print(related_damages)
        else:#  len(elem_name) > 1 and len(elem_number) > 1: # {'first': [['排水管 Dp0101', '排水管 Dp0102']], 'second': [['①腐食(小大)-c', '⑤防食機能の劣化(分類1)-e']]}
            #print(first_item) # ['排水管 Dp0101', '排水管 Dp0102']
            #print(second_item) # ['①腐食(小大)-c', '⑤防食機能の劣化(分類1)-e']
            related_damage_list = ','.join(second_item)
            #print(related_damage_list)
            processed_related_damages.append(f"{','.join(elem_name)}:{related_damage_list}")
            #print(related_damages)


    related_description = ""
    if processed_related_damages:
        related_description = "\n【関連損傷】\n" + ", ".join(processed_related_damages)

    return f"{primary_description} {related_description}".strip()

print(generate_report(item))