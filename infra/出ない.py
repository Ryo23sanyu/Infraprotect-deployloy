import re


request_list = {'first': [['支承本体 Bh0101'], ['沓座モルタル Bm0101']], 'second': [['①腐食(小小)-b', '㉓変形・欠損-c'], ['⑦剥離・鉄筋露出-c']]}
#request_list = {'first': [['排水管 Dp0101']], 'second': [['①腐食(大大)-e'], ['⑤防食機能の劣化(分類1)-e']]}

# <<◆ secondの多重リストを統一させる ◆>>
try:
    check_request_list = request_list['first'][1]
    print(check_request_list)

    # 条件分岐
    if isinstance(check_request_list, list):
        test = request_list
        print(f"request_list：{request_list}")
        
except (KeyError, IndexError) as e:
    # KeyError や IndexError の例外が発生した場合の処理

    # secondの多重リストをフラットなリストに変換
    flat_list = [item for sublist in request_list['second'] for item in sublist]
    # フラットなリストを再びサブリストに変換して格納
    request_list['second'] = [flat_list]
    # 完成目標の確認
    
    test = request_list['second'][0]
    print(f"test:{test}")

# 先頭が文字（日本語やアルファベットなど）の場合
def all_match_condition(lst):
    """
    リスト内のすべての項目が特定条件に一致するか確認します。
    ただし、空のリストの場合、Falseを返します。
    """
    # 空のリストの場合は False を返す
    if not lst:
        return False
    
    pattern = re.compile(r'\A[^\W\d_]', re.UNICODE)
    return all(pattern.match(item) for item in lst)

if all_match_condition(test):
    request_list
else:
    request_list['second'] = [request_list['second']]

#<< ◆損傷メモの作成◆ >>
replacement_patterns = {
    "①腐食(小小)-b": "腐食", # 1
    "⑦剥離・鉄筋露出-c": "コンクリートの剥離", # 7
    "㉓変形・欠損-c": "変形・欠損", # 23
}

def describe_damage(unified_request_list):
    described_list = []
    print(f"unified_request_list：{unified_request_list}")
    for damage in unified_request_list:
        if damage in replacement_patterns:
            described_list.append(replacement_patterns[damage])
            print(f"described_list：{described_list}")
        elif damage.startswith('⑰'):
            match = re.search(r'(?<=:)(.*?)(?=\)-e)', damage)
            if match:
                described_list.append(match.group(1))
                print(f"described_list：{described_list}")
        else:
            pattern = r'[\u3248-\u3257](.*?)-'
            match = re.search(pattern, damage)
            if match:
                described_list.append(match.group(1))
                print(f"described_list：{described_list}")
            else:
                described_list.append(damage)  # フォールバックとしてそのまま返す
                print(f"described_list：{described_list}")
    return ','.join(described_list)
# メイン処理部分で describe_damage を呼び出し
try:
    unified_request_list = [item for sublist in request_list['second'] for item in sublist]
    damage_description = describe_damage(unified_request_list)
    print(f"Damage Description: {damage_description}")
except Exception as e:
    print(f"An error occurred: {e}")
# 各ケースに対して出力を確認:
def generate_report(unified_request_list):
    primary_damages = []
    processed_related_damages = []
    print(f"unified_request_list：{unified_request_list}")
    first_items = unified_request_list['first']
    print(first_items) # [['支承本体 Bh0101'], ['沓座モルタル Bm0101']]
    second_items = unified_request_list['second']
    print(second_items) # [['①腐食(小小)-b', '⑤防食機能の劣化(分類1)-e'], ['⑦剥離・鉄筋露出-c']]
    primary_damages_dict = {}

    for first_item, second_item in zip(first_items, second_items):
        print(f"first_items：{first_items}")
        print(f"second_items：{second_items}")
        print(f"first_item：{first_item}")
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
    print(primary_description)
        
    for elem_name, elem_number in zip(first_items, second_items): # 主桁 Mg0101
        print(f"{first_items}-{elem_name}") # でない
        print(f"{second_items}-{elem_number}")
        print(len(first_items))
        print(len(second_items))
        #print(" ")
        # リストをフラットにする関数
        def flatten_list(nested_list):
            return [item for sublist in nested_list for item in sublist]
        
        # 辞書から 'first' と 'second' の値を取り出す
        first_list = request_list['first']
        second_list = request_list['second']

        # 'first' の要素数を数える
        first_count = sum(len(sublist) for sublist in first_list)

        # 'second' の要素数を数える
        second_count = sum(len(sublist) for sublist in second_list)
        # フラットにしたリストを比較
        if flatten_list(first_items) != elem_name and flatten_list(second_items) != elem_number:
            #print(f"{flatten_list(first_items)}-{elem_name}")
            #print(f"{flatten_list(second_items)}-{elem_number}")
            sub_related_damages = []
            for first_item in first_items:
                for elem in first_item:
                    if elem in primary_damages_dict:
                        formatted_damages = ",".join(list(dict.fromkeys(primary_damages_dict[elem])))
                        sub_related_damages.append(f"{elem}:{formatted_damages}")
                        #print(f"sub_related_damages：{sub_related_damages}") # ['支承本体 Bh0101:①腐食(小小)-b,⑤防食機能の劣化(分類1)-e', '沓座モルタル Bm0101:⑦剥離・鉄筋露出-c']

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
            
        elif first_count < 2 and second_count < 2: # {'first': [['横桁 Cr0803']], 'second': [['⑦剥離・鉄筋露出-d']]}
            None
        elif first_count > 1 and second_count < 2: # {'first': [['床版 Ds0201', '床版 Ds0203']], 'second': [['⑦剥離・鉄筋露出-d']]}
            #print(f"first_item：{first_item}") # ['床版 Ds0201', '床版 Ds0203']
            #print(f"second_item：{second_item}") # ['⑦剥離・鉄筋露出-d']
            first_items_from_first = first_item[1:]
            #print(first_items_from_first) # ['橋台[竪壁] Ac0101', '伸縮装置 Ej0101']
            related_damage_list = ','.join(first_items_from_first)# カンマ区切りの文字列に結合
            #print(related_damage_list) # 橋台[竪壁] Ac0101,伸縮装置 Ej0101
            related_second_item = ','.join(second_item)
            processed_related_damages.append(f"{related_damage_list}:{related_second_item}")
            #print(f"2-1_processed_related_damages：{processed_related_damages}")
        elif first_count < 2 and second_count > 1: # {'first': [['横桁 Cr0503']], 'second': [['⑦剥離・鉄筋露出-d', '⑰その他(分類6:施工不良)-e']]}
            #print(first_item) # ['横桁 Cr0503']
            #print(second_item) # ['⑦剥離・鉄筋露出-d', '⑰その他(分類6:施工不良)-e']
            second_items_from_second = second_item[1:]
            related_damage_list = ','.join(second_items_from_second)# カンマ区切りの文字列に結合
            #print(related_damage_list)
            processed_related_damages.append(f"{','.join(elem_name)}:{related_damage_list}")
            #print(f"1-2_processed_related_damages：{processed_related_damages}")
        else:#  len(elem_name) > 1 and len(elem_number) > 1: # {'first': [['排水管 Dp0101', '排水管 Dp0102']], 'second': [['①腐食(小大)-c', '⑤防食機能の劣化(分類1)-e']]}
            #print(first_item) # ['排水管 Dp0101', '排水管 Dp0102']
            #print(second_item) # ['①腐食(小大)-c', '⑤防食機能の劣化(分類1)-e']
            related_damage_list = ','.join(second_item)
            #print(related_damage_list)
            processed_related_damages.append(f"{','.join(elem_name)}:{related_damage_list}")
            #print(f"0-0_processed_related_damages：{processed_related_damages}")


    related_description = ""
    if processed_related_damages:
        related_description = "\n【関連損傷】\n" + ", ".join(processed_related_damages)

    return f"{primary_description} {related_description}".strip()