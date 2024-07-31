# << 所見一覧 >>
def observations_list(request, article_pk, pk):
    context = {}

    table = Table.objects.filter(id=pk).first()
    # print(f"table_name{table}")

    if table.dxf:
        encoded_url_path = table.dxf.url
    decoded_url_path = urllib.parse.unquote(encoded_url_path)
    # 絶対パスと合体
    dxf_filename = os.path.join(settings.BASE_DIR, decoded_url_path.lstrip('/'))
    
    context["object"] = table
    context["buttons"] = table.infra.径間数 * " "
    
    if "search_title_text" in request.GET:
        search_title_text = request.GET["search_title_text"]
    else:
        search_title_text = "1径間"

    second_search_title_text = "損傷図"
    
    sorted_items = create_picturelist(request, table, dxf_filename, search_title_text, second_search_title_text)
    
    
    # TODO:関数化して、別コードでも使用できるようにする
    """番号登録のデータを別の(FullReportData)モデルに合体させる"""
    """損傷写真帳のデータと番号登録のデータを合体、重複の削除と並び替え"""
    result_items = []

    for item in sorted_items:
        join_items = item.get('join', [])
        pictures = item.get('this_time_picture', [])
        
        # 各 join 要素に picture を追加
        for join_item in join_items:
            join_item['this_time_picture'] = pictures
        
        result_items.append({'join': join_items})

    # joinキーのみを抽出
    join_values = [item['join'] for item in result_items]

    # join値を1行にまとめる
    flattened_join = [join_item for sublist in join_values for join_item in sublist]

    # << 番号登録のデータを呼び出す >>
    parts_numbers = PartsNumber.objects.filter(infra=pk)
    print(f"parts_numbers：{parts_numbers}")
    number_create = []

    for parts_number in parts_numbers:
        dic = {}

        dic['parts_name'] = [parts_number.parts_name.部材名]
        dic['symbol'] = [parts_number.symbol]
        dic['number'] = [parts_number.number]

        materials = ""
        for material in parts_number.material.all():
            materials += material.材料 + ":"

        # 鋼、その他、プラスチックの場合
        # 鋼:その他:プラスチック: になる。
        # 最後の1文字を取り除いた文字を新しいmaterialsに入れる。

        materials = materials[:-1]
        dic['material'] = [materials]

        if parts_number.main_frame:
            dic['main_frame'] = ["〇"]
        else:
            dic['main_frame'] = ["✕"]

        number_create.append(dic)
        
    print(f"number_create:{number_create}")
    print(f"flattened_join:{flattened_join}")
    
    # << 材料の置換 >>
    replace_dict = {
        '鋼': 'S',
        'コンクリート': 'C',
        'その他': 'X'
    }

    # 置換処理
    for part in number_create:
        part['material'] = [replace_dict.get(mat, mat) for mat in part['material']]
        # parts_name と symbol の各要素を結合して新しいリストを作成
        combined = [p + ' ' + s for p, s in zip(part['parts_name'], part['symbol'])]
        # 新しいリストを parts_name に設定（symbol は削除）
        part['parts_name'] = combined
        del part['symbol']

    # << parts_nameを部材名と番号に分割 >>
    split_parts_and_damage = []

    # 各要素に対して処理を行う
    for item in flattened_join:
        combined_string = item['parts_name'][0]
        
        # 正規表現を使って、記号と数字の部分で分割する
        match = re.match(r'(.+ [A-Za-z]+)(\d+)', combined_string)
        
        if match:
            parts_name = match.group(1)
            number = match.group(2)
            
            for damage in item['damage_name']:
                if "-" in damage:
                    damage_name, damage_lank = damage.split("-")
                
                parts_dict = {
                    'parts_name': [parts_name],
                    'number': [number],
                    'damage_name': [damage_name],
                    'damage_lank': [damage_lank],
                    'this_time_picture': item['this_time_picture']  # this_time_pictureを追加
                }
                split_parts_and_damage.append(parts_dict)

    # << 2つのリストを合体 >>
    def sort_and_merge_list(ordered_result, order_dict, material_dict, order_number, order_lank):
        # ソートキーの設定
        def sort_key(item):
            # parts_nameのソートキー
            parts_name_key = order_dict.get(item['parts_name'][0].split()[0], 0)
            
            # numberのソートキー
            number_key = int(item['number'][0]) if item['number'] and item['number'][0].isdigit() else 0
            
            # damage_nameのソートキー (最初の1文字を使用)
            damage_name_initial = item['damage_name'][0][0] if item['damage_name'] else "None"
            damage_name_key = order_number.get(damage_name_initial, 0)
            
            # damage_lankのソートキー
            damage_lank_key = order_lank.get(item['damage_lank'][0], 0) if item['damage_lank'] else 0
            
            return parts_name_key, number_key, damage_name_key, damage_lank_key

        # リストをソート
        ordered_result = sorted(ordered_result, key=sort_key)

        # 重複および合体の処理
        merged_result = []
        for item in ordered_result:
            # 重複をチェックしてマージするか新規追加するか決定
            if not merged_result:
                merged_result.append(item)
            else:
                last_item = merged_result[-1]
                if (last_item['parts_name'] == item['parts_name'] and 
                    last_item['number'] == item['number'] and 
                    last_item['damage_name'] == item['damage_name'] and
                    last_item['main_frame'] == item['main_frame']):
                    
                    # materialの合体
                    if last_item['material'] and item['material']:
                        last_item['material'] = list(set(last_item['material'] + item['material']))
                    elif item['material']:
                        last_item['material'] = item['material']
                    
                    # damage_lankの合体
                    if last_item['damage_lank'] and item['damage_lank']:
                        last_item['damage_lank'] = list(set(last_item['damage_lank'] + item['damage_lank']))
                    elif item['damage_lank']:
                        last_item['damage_lank'] = item['damage_lank']
                else:
                    merged_result.append(item)

        return merged_result

    # 結果格納用のリスト
    result = []

    # sorted_splitをループし、number_createと比較
    for item in split_parts_and_damage:
        found = False
        for nc_item in number_create:
            if item['parts_name'] == nc_item['parts_name'] and item['number'] == nc_item['number']:
                item.update({'material': nc_item['material'], 'main_frame': nc_item['main_frame']})
                found = True
                break
        if 'material' not in item:
            item['material'] = None
        if 'main_frame' not in item:
            item['main_frame'] = None
        result.append(item)

    # number_createの項目を結果に追加
    for nc_item in number_create:
        # sorted_splitに存在しない場合のチェック
        exists = any(item['parts_name'] == nc_item['parts_name'] and item['number'] == nc_item['number'] for item in split_parts_and_damage)
        if not exists:
            result.append({'parts_name': nc_item['parts_name'], 'number': nc_item['number'], 'material': nc_item['material'], 'main_frame': nc_item['main_frame'], 'this_time_picture': None})

    # 指定した順番でキーを整列
    ordered_result = []
    ordered_keys = ['parts_name', 'number', 'material', 'damage_lank', 'damage_name', 'main_frame', 'this_time_picture']

    for item in result:
        ordered_item = {key: item.get(key) for key in ordered_keys}
        ordered_result.append(ordered_item)

    # 入力データ

    order_dict = {"主桁": 1, "横桁": 2, "床版": 3, "PC定着部": 4, "橋台[胸壁]": 5, "橋台[竪壁]": 6, "支承本体": 7, "沓座モルタル": 8, "防護柵": 9, "地覆": 10, "伸縮装置": 11, "舗装": 12, "排水ます": 13, "排水管": 14}
    material_dict = {"S": 1, "C": 2, "X": 3}
    order_number = {"None": 0, "①": 1, "②": 2, "③": 3, "④": 4, "⑤": 5, "⑥": 6, "⑦": 7, "⑧": 8, "⑨": 9, "⑩": 10, "⑪": 11, "⑫": 12, "⑬": 13, "⑭": 14, "⑮": 15, "⑯": 16, "⑰": 17, "⑱": 18, "⑲": 19, "⑳": 20, "㉑": 21, "㉒": 22, "㉓": 23, "㉔": 24, "㉕": 25, "㉖": 26}
    order_lank = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}

    # ソートとマージ
    flattened_join_result = sort_and_merge_list(ordered_result, order_dict, material_dict, order_number, order_lank)
    """"""
    
    # << 部材名と要素番号を結合 >>
    for item in flattened_join_result:
        combined = [p_n  + num for p_n, num in zip(item['parts_name'], item['number'])]
        # 新しいリストを parts_name に設定
        item['parts_name'] = combined
        del item['number'] # キーの削除
    
    main_parts_list_left = ["主桁", "PC定着部"] # 左の数字
    main_parts_list_right = ["横桁", "橋台"] # 右の数字
    main_parts_list_zero = ["床版"] # 00になる場合

    # データをグループ化するための辞書
    grouped_data = defaultdict(lambda: defaultdict(lambda: {'lanks': [], 'pictures': [], 'main_frame': []}))

    def process_item(item):
        name_and_number = item['parts_name'][0]
        
        if any(word in name_and_number for word in main_parts_list_left):
            left = name_and_number.find(" ")
            number2 = name_and_number[left+1:]
            number_part = re.search(r'[A-Za-z]*(\d+)', number2).group(1)
            parts_name = name_and_number[:left]+" "+number_part[:2] # 主桁 03
        elif any(word in name_and_number for word in main_parts_list_right):
            right = name_and_number.find(" ")
            number2 = name_and_number[right+1:]
            number_part = re.search(r'[A-Za-z]*(\d+)', number2).group(1)
            if len(number_part) < 5:
                parts_name = name_and_number[:right]+" "+number_part[2:] # 横桁 02
            else:
                parts_name = name_and_number[:right]+" "+number_part[2:] # 横桁 103
        elif any(word in name_and_number for word in main_parts_list_zero):
            right = name_and_number.find(" ")
            parts_name = name_and_number[:right]+" 00"
        else:
            right = name_and_number.find(" ")
            parts_name = name_and_number[:right]
        
        # << 損傷名の設定 >>
        in_damage = item['damage_name']
        if in_damage == None:
            damage = "NON"
        else:
            damage = ''.join(in_damage)
        
        if damage.startswith('⑰'):
            damage_name = damage
        else:
            first_parenthesis_index = damage.find('(')
            if first_parenthesis_index != -1:  # カッコが見つかった場合
                damage_name = damage[:first_parenthesis_index][1:]
            elif damage == "NON":
                damage_name = damage
            else:
                damage_name = damage[1:]
        # print(f"damage_name:{damage_name}")
        
        # << 損傷ランクの設定 >>
        before_damage_lank = item['damage_lank']
        if before_damage_lank is not None:
            damage_lank = ','.join(before_damage_lank)
        else:
            damage_lank = 'a'
        # print(f"damage_lank：{damage_lank}")
        
        grouped_data[parts_name][damage_name]['lanks'].append(damage_lank)
        if item['this_time_picture']:
            grouped_data[parts_name][damage_name]['pictures'].extend(item['this_time_picture'])
        if item['main_frame'] == ['〇']:
            grouped_data[parts_name][damage_name]['main_frame'].extend(item['main_frame'])
        
    for item in flattened_join_result:
        process_item(item)

    # 重複削除と並び替えを行う関数
    def unique_sorted_lanks(lanks, order_lank):
        unique_lanks = list(sorted(set(lanks), key=lambda x: order_lank[x]))
        return unique_lanks

    # 新しいリストを作成
    order_lank = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
    
    change_observer_list = [
        {'parts_name': [parts], 'damage_name': [damage], 'damage_lank': unique_sorted_lanks(damages['lanks'], order_lank), 'this_time_picture': list(set(damages['pictures'])), 'main_frame': list(set(damages['main_frame']))}
        for parts, damages in grouped_data.items()
        for damage, damages in damages.items()
    ]
    
    for change_key_item in change_observer_list:
        # 'lank'キーがリストの場合はハイフンでつなげる
        if isinstance(change_key_item['damage_lank'], list):
            change_key_item['damage_lank'] = '～'.join(change_key_item['damage_lank'])
        # 'lank'キーが単一の文字列の場合はそのままにする
        elif isinstance(change_key_item['damage_lank'], str):
            change_key_item['damage_lank'] = change_key_item['damage_lank']

    print(f"change_observer_list:{change_observer_list}")

    return render(request, 'observer_list.html', {'data': change_observer_list, 'article_pk': article_pk, 'pk': pk})