# << 損傷写真帳の作成 >>
def bridge_table(request, article_pk, pk): # idの紐付け infra/bridge_table.htmlに表示
    context = {}
    # プロジェクトのメディアディレクトリからdxfファイルまでの相対パス
    # URL：article/<int:article_pk>/infra/<int:pk>/bridge-table/
    table = Table.objects.filter(id=pk).first()
    print(f"table_name:{table}") # Table object (17)
    print(f"table.infra.title:{table.infra.title}")
    infra_instance = Infra.objects.filter(title = table.infra.title)
    print(f"table_name:{infra_instance}") # センサス橋

    if table.dxf:
        encoded_url_path = table.dxf.url
    decoded_url_path = urllib.parse.unquote(encoded_url_path) # URLデコード
    dxf_filename = os.path.join(settings.BASE_DIR, decoded_url_path.lstrip('/'))
    
    # bridge_tableのボタンを押したときのアクション
    if "search_title_text" in request.GET:
        # request.GET：検索URL（http://127.0.0.1:8000/article/1/infra/bridge_table/?search_title_text=1径間） 
        search_title_text = request.GET["search_title_text"]
        # 検索URL内のsearch_title_textの値（1径間）を取得する
    else:
        search_title_text = "1径間" # 検索URLにsearch_title_textがない場合

    second_search_title_text = "損傷図"
    
    # sorted_items = create_picturelist(request, table, dxf_filename, search_title_text, second_search_title_text)

    # << 辞書型として、全径間を1つの多重リストに格納 >>
    max_search_title_text = table.infra.径間数
    database_sorted_items = []  # 結果をまとめるリスト
    
    for search_title_text_with_suffix in range(1, max_search_title_text + 1):
        search_title_text = f"{search_title_text_with_suffix}径間"
        sub_database_sorted_items = create_picturelist(request, table, dxf_filename, search_title_text, second_search_title_text)
        for item in sub_database_sorted_items:
            item['search'] = search_title_text
            database_sorted_items.append(item)
    # print(f"database_sorted_items:{database_sorted_items}")
    """辞書型の多重リストをデータベースに登録"""
    # << ['']を外してフラットにする >>
    def flatten(value):
        def _flatten(nested_list):
            if isinstance(nested_list, list):
                for item in nested_list:
                    yield from _flatten(item)
            else:
                yield nested_list
        
        return ', '.join(_flatten(value))

    # << joinキーを変換 >>
    def join_to_result_string(join):
        result_parts = []
        for item in join:
            parts_name = item['parts_name'][0]
            damage_names = item['damage_name']
            formatted_damage_names = '/'.join(damage_names)
            result_parts.append(f"{parts_name} : {formatted_damage_names}")
        return ', '.join(result_parts)

    # << 写真のキーを変換 >>
    def simple_flatten(value):
        return ', '.join(map(str, value)) if isinstance(value, list) else value
    
    # <<正規表現で4桁以上の番号を取得>>
    def extract_number(text):
        pattern = r'\d{4,}' # 4文字以上の連続する数字
        matches = re.findall(pattern, text)
        return matches
    
    for damage_data in database_sorted_items:
        #print(f"damage_data：{damage_data}")
        # 元の辞書から 'picture_number' の値を取得
        #             　辞書型 ↓           ↓ キーの名前      ↓ 存在しない場合、デフォルト値として空白を返す
        picture_number = damage_data.get('picture_number', '')
        # 正規表現で数字のみを抽出
        if picture_number:
            # 数字のみを抽出
            numbers_only = re.findall(r'\d+', str(picture_number)) # ['2']
            # 数字を結合して整数に変換
            numbers_only = int(''.join(numbers_only)) if numbers_only else None # 2
        else:
            numbers_only = None

        damage_coordinate = damage_data.get('damage_coordinate', [None, None])
        picture_coordinate = damage_data.get('picture_coordinate', [None, None])
        names = damage_data.get('parts_name', '')
        damages = damage_data.get('damage_name', '')

        split_names = []

        for item in names:
            split_items = []
            for split in item:
                if "～" in split:
                    one = split.find("～")
                    start_number = ''.join(extract_number(split[:one])) # 0101
                    end_number = ''.join(extract_number(split[one+1:])) # 0204

                    # 最初の2桁と最後の2桁を取得
                    start_prefix = start_number[:2] # 01
                    start_suffix = start_number[2:] # 01
                    end_prefix = end_number[:2] # 01
                    end_suffix = end_number[2:] # 03
                    
                    part_name = split[:one].replace(start_number, '')
                
                    for prefix in range(int(start_prefix), int(end_prefix)+1):
                        for suffix in range(int(start_suffix), int(end_suffix)+1):
                            number_items = "{:02d}{:02d}".format(prefix, suffix)
                            join_item = part_name + number_items
                            split_items.append(join_item)
                    
                else:
                    split_items.append(split)
            split_names.append(split_items)
        
        join = join_to_result_string(damage_data.get('join', ''))
        this_time_picture = simple_flatten(damage_data.get('this_time_picture', ''))
        last_time_picture = simple_flatten(damage_data.get('last_time_picture', ''))
        textarea_content = damage_data.get('textarea_content', '')
        damage_coordinate_x = damage_coordinate[0] if damage_coordinate else None
        damage_coordinate_y = damage_coordinate[1] if damage_coordinate else None
        picture_coordinate_x = picture_coordinate[0] if picture_coordinate else None
        picture_coordinate_y = picture_coordinate[1] if picture_coordinate else None
        span_number = damage_data.get('search', '')
        
        name_length = len(split_names)
        damage_length = len(damages)
        
        # 多重リストかどうかを判定する関数
        def is_multi_list(lst):
            return any(isinstance(i, list) for i in lst)
        
        def process_names(names):          
            parts_left = ["主桁", "PC定着部"]  # 左の数字
            parts_right = ["横桁", "橋台"]     # 右の数字
            parts_zero = ["床版"]              # 00になる場合

            # namesから部品名（parts）と数字を抽出
            space = names.find(" ")
            parts = names[:space]  # 部品名
            number = ''.join(extract_number(names))  # 数字
            parts_join = names.replace(number, '') # 符号部分を取得

            # 必要な部分の数字を抽出するロジック
            split_number = ''

            if parts in parts_zero:
                split_number = '00'
            elif len(number) == 4 or int(number[2:]) >= 100:
                if parts in parts_left:
                    split_number = number[:2]
                elif parts in parts_right:
                    split_number = number[2:]
                else:
                    split_number = '00'
            else:
                if parts in parts_left:
                    split_number = number[:3]
                elif parts in parts_right:
                    split_number = number[3:]
                else:
                    split_number = '00'

            result = parts_join + split_number  # 結果を組み立てる
            return result
            # 共通のフィールドを辞書に格納
        
        if not is_multi_list(split_names) and not is_multi_list(damages) and name_length == 1: # 部材名が1つの場合
            for single_damage in damages: 
                parts_name = names[0]
                damage_name = flatten(single_damage)
                #print(f"parts_name1:{parts_name}")
                #print(f"damage_name1:{damage_name}")
                parts_split = process_names(flatten(parts_name))
                data_fields = {
                    'parts_name': parts_name,
                    'damage_name': damage_name,
                    'parts_split': parts_split,
                    'join': join,
                    'picture_number': numbers_only,
                    'this_time_picture': this_time_picture,
                    'last_time_picture': last_time_picture,
                    'textarea_content': textarea_content,
                    'damage_coordinate_x': damage_coordinate_x,
                    'damage_coordinate_y': damage_coordinate_y,
                    'picture_coordinate_x': picture_coordinate_x,
                    'picture_coordinate_y': picture_coordinate_y,
                    'span_number': span_number,
                    'special_links': '/'.join([str(parts_split), str(damage_name), str(span_number)]),
                    'infra': Infra.objects.get(id=pk)
                }
                report_data_exists = FullReportData.objects.filter(**data_fields).exists()
                if report_data_exists:
                    print("データが存在しています。")
                else:
                    try:
                        damage_obj, created = FullReportData.objects.update_or_create(**data_fields)
                        damage_obj.save()
                    except IntegrityError:
                        print("ユニーク制約に違反していますが、既存のデータを更新しませんでした。")

        elif not is_multi_list(split_names) and not is_multi_list(damages) and name_length >= 2: # 部材名が2つ以上の場合
            if damage_length == 1: # かつ損傷名が1つの場合
                for single_name in split_names:
                    parts_name = single_name
                    damage_name = flatten(damages[0])
                    #print(f"parts_name2:{parts_name}")
                    #print(f"damage_name2:{damage_name}")
                    parts_split = process_names(flatten(parts_name))
                    data_fields = {
                        'parts_name': parts_name,
                        'damage_name': damage_name,
                        'parts_split': parts_split,
                        'join': join,
                        'picture_number': numbers_only,
                        'this_time_picture': this_time_picture,
                        'last_time_picture': last_time_picture,
                        'textarea_content': textarea_content,
                        'damage_coordinate_x': damage_coordinate_x,
                        'damage_coordinate_y': damage_coordinate_y,
                        'picture_coordinate_x': picture_coordinate_x,
                        'picture_coordinate_y': picture_coordinate_y,
                        'span_number': span_number,
                        'special_links': '/'.join([str(parts_split), str(damage_name), str(span_number)]),
                        'infra': Infra.objects.get(id=pk)
                    }
                    report_data_exists = FullReportData.objects.filter(**data_fields).exists()
                    if report_data_exists:
                        print("データが存在しています。")
                    else:
                        try:
                            damage_obj, created = FullReportData.objects.update_or_create(**data_fields)
                            damage_obj.save()
                        except IntegrityError:
                            print("ユニーク制約に違反していますが、既存のデータを更新しませんでした。")

            elif not is_multi_list(split_names) and not is_multi_list(damages) and damage_length >= 2: # かつ損傷名が2つ以上の場合
                for name in split_names:
                    for damage in damages:
                        parts_name = name
                        damage_name = flatten(damage)
                        #print(f"parts_name3:{parts_name}")
                        #print(f"damage_name3:{damage_name}")
                        parts_split = process_names(flatten(parts_name))
                        data_fields = {
                            'parts_name': parts_name,
                            'damage_name': damage_name,
                            'parts_split': parts_split,
                            'join': join,
                            'picture_number': numbers_only,
                            'this_time_picture': this_time_picture,
                            'last_time_picture': last_time_picture,
                            'textarea_content': textarea_content,
                            'damage_coordinate_x': damage_coordinate_x,
                            'damage_coordinate_y': damage_coordinate_y,
                            'picture_coordinate_x': picture_coordinate_x,
                            'picture_coordinate_y': picture_coordinate_y,
                            'span_number': span_number,
                            'special_links': '/'.join([str(parts_split), str(damage_name), str(span_number)]),
                            'infra': Infra.objects.get(id=pk)
                        }
                        report_data_exists = FullReportData.objects.filter(**data_fields).exists()
                        if report_data_exists:
                            print("データが存在しています。")
                        else:
                            try:
                                damage_obj, created = FullReportData.objects.update_or_create(**data_fields)
                                damage_obj.save()
                            except IntegrityError:
                                print("ユニーク制約に違反していますが、既存のデータを更新しませんでした。")

        else: # 多重リストの場合
            for i in range(name_length):
                for name in split_names[i]:
                    for damage in damages[i]:
                        parts_name = name
                        damage_name = flatten(damage)
                        #print(f"parts_name4:{parts_name}")
                        #print(f"damage_name4:{damage_name}")
                        parts_split = process_names(flatten(parts_name))
                        data_fields = {
                            'parts_name': parts_name,
                            'damage_name': damage_name,
                            'parts_split': parts_split,
                            'join': join,
                            'picture_number': numbers_only,
                            'this_time_picture': this_time_picture,
                            'last_time_picture': last_time_picture,
                            'textarea_content': textarea_content,
                            'damage_coordinate_x': damage_coordinate_x,
                            'damage_coordinate_y': damage_coordinate_y,
                            'picture_coordinate_x': picture_coordinate_x,
                            'picture_coordinate_y': picture_coordinate_y,
                            'span_number': span_number,
                            'special_links': '/'.join([str(parts_split), str(damage_name), str(span_number)]),
                            'infra': Infra.objects.get(id=pk)
                        }
                        report_data_exists = FullReportData.objects.filter(**data_fields).exists()
                        if report_data_exists:
                            print("データが存在しています。")
                        else:
                            try:
                                damage_obj, created = FullReportData.objects.update_or_create(**data_fields)
                                damage_obj.save()
                            except IntegrityError:
                                print("ユニーク制約に違反していますが、既存のデータを更新しませんでした。")

    """辞書型の多重リストをデータベースに登録(ここまで)"""
    # path('article/<int:article_pk>/infra/<int:pk>/bridge-table/', views.bridge_table, name='bridge-table')

    #context["damage_table"] = sorted_items
    #return render(request, "infra/bridge_table.html", context)

    # # テンプレートをレンダリング
    # return render(request, 'infra/bridge_table.html', context)
    bridges = FullReportData.objects.filter(infra=pk, span_number=search_title_text)

    # HTMLにまとめて表示するためのグループ化
    grouped_data = []
    for key, group in groupby(bridges, key=attrgetter('join', 'damage_coordinate_x', 'damage_coordinate_y')):
        grouped_data.append(list(group))

    # buttons = table.infra.径間数 * " "
    buttons = "1径間"
    print(f"max_search_title_texts:{max_search_title_text}")

    context = {'object': Table.objects.filter(id=pk).first(), 'grouped_data': grouped_data, 'buttons': buttons}

    return render(request, 'infra/bridge_table.html', context)