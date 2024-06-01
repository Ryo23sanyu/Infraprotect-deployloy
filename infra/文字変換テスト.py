import re

request_list = {'first': [['排水管 Dp0102']], 'second': [['①腐食(小大)-c'], ['⑤防食機能の劣化(分類1)-e']]}

#<< ◆損傷メモの作成◆ >>
replacement_patterns = {
}

def describe_increase_damage(request_list):
    # 新しい辞書を作成する
    unified_request_list = {}

    for key, damages in request_list.items():
        # 各キーに対する新しい統一されたリスト
        unified_damage_list = []

        for damage in damages:
            if isinstance(damage, str):
                # 文字列の場合はリストに変換して追加
                unified_damage_list.append([damage])
            else:
                # 既にリスト形式の場合はそのまま追加
                unified_damage_list.append(damage)

        # 新しい辞書に追加
        unified_request_list[key] = unified_damage_list

    # 結果を表示
    print(unified_request_list)

describe_increase_damage(request_list)

def describe_damage(unified_request_list):
    described_list = []
    
    for damage in unified_request_list:
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
def generate_report(unified_request_list):
    primary_damages = []
    processed_related_damages = []
    print(f"unified_request_list：{unified_request_list}")
    first_items = unified_request_list['first']
    #print(first_items) # [['支承本体 Bh0101'], ['沓座モルタル Bm0101']]
    second_items = unified_request_list['second']
    #print(second_items) # [['①腐食(小小)-b', '⑤防食機能の劣化(分類1)-e'], ['⑦剥離・鉄筋露出-c']]
    primary_damages_dict = {}

    for first_item, second_item in zip(first_items, second_items):
        #print(f"first_items：{first_items}")
        #print(f"second_items：{second_items}")
        #print(f"first_item：{first_item}")
        print(f"second_item：{second_item}")
        element_names = [f.split()[0] for f in first_item] # カッコ内の要素について、スペースより前を抽出
        print(f"element_names：{element_names}") # ['支承本体'], ['沓座モルタル']
        damage_descriptions = describe_damage(second_item) # 辞書で置換
        print(f"damage_descriptions：{damage_descriptions}") # 腐食,点錆, 剥離
        
        if len(element_names) == 1: # ['主桁', '横桁', '対傾構']：これはだめ
            primary_damages.append(f"{element_names[0]}に{damage_descriptions}が見られる。")
            #print(f"primary_damages：{primary_damages}") # ['支承本体に腐食,点錆が見られる。', '沓座モルタルに剥離が見られる。']
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
                        print(f"sub_related_damages：{sub_related_damages}") # ['支承本体 Bh0101:①腐食(小小)-b,⑤防食機能の劣化(分類1)-e', '沓座モルタル Bm0101:⑦剥離・鉄筋露出-c']

            # 処理後のリストを格納するための新しいリスト
            second_related_damages = []

            # リスト内の各要素をループする
            for i, damage in enumerate(sub_related_damages):
                # コロンの位置を取得
                colon_index = damage.find(":")
                
                if colon_index != -1:
                    if i == 0:
                        # 1番目の要素の場合
                        parts = damage.split(',')
                        
                        if len(parts) > 1:
                            first_damage = parts[0].split(':')[0]
                            after_damage = ':' + parts[1].strip()
                            create_damage = first_damage + after_damage
                            second_related_damages.append(create_damage)

                    else:
                        # 2つ目以降の要素の場合
                        parts = damage.split(',')
                        second_related_damages.append(damage)
                        

            # 処理後のリストを格納するための新しいリスト
            processed_related_damages = []
            #print(f"second_related_damages：{second_related_damages}")
            for damage in second_related_damages:
                colon_index = damage.find(":")
                if colon_index != -1:
                    before_colon_part = damage[:colon_index].strip()
                    after_colon_part = damage[colon_index + 1:].strip()
                    #print(f"damage[colon_index + 1:]：{damage}")
                    if before_colon_part and after_colon_part:
                        processed_damage = f"{before_colon_part}:{after_colon_part}"
                        processed_related_damages.append(processed_damage)
            #print(f"after_colon_part：{processed_related_damages}")
            
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

combined_data = generate_report(request_list)
print(combined_data)

# << ◆ ここまで ◆ >>                   
        # \n文字列のときの改行文字
#items = {'first': first_item[i], 'second': second_items[i], 'join': first_and_second, 'third': third, 'last': picture_urls, 'picture': 'infra/noImage.png', 'textarea_content': combined_data, 'damage_coordinate': damage_coordinate[i], 'picture_coordinate': picture_coordinate[i]}
#items = {'first': first_item[i], 'second': second_items[i]}
#print(items)
#print("")