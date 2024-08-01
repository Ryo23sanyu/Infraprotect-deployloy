
for part in parts_data:
    part_full_name = f"{part.parts_name} {part.symbol}{part.number}"
    span_number = part.span_number + '径間'

    # FullReportDataから部材名(主桁 Mg0101)、径間名、橋名が一致するデータを取得
    report_data_list = FullReportData.objects.filter(
        parts_name=part_full_name,
        span_number=span_number,
        infra=part.infra
    )
    
    # 全損傷から各損傷に分解(forループ)
    for report_data in report_data_list:
        # 対象材料を取得し、記号に置換
        damage_list_material = ""
        for m in part.material.all():
            damage_list_material += m.材料 + ","
        elements = damage_list_material.split(',')
        replaced_elements = [material_replace_map.get(element, element) for element in elements]
        damage_list_materials = ','.join(replaced_elements)
        # 損傷名を26個に分類する(その他のみ別)
        damage_name = report_data.damage_name.split('-')[0] if '-' in report_data.damage_name else report_data.damage_name
        if damage_name == "NON":
            damage_name = damage_name
        elif damage_name[0] != '⑰':
            damage_name = number_change[damage_name[0]]
        else:
            damage_name = damage_name[1:]
        # a～eを取得    
        damage_lank = report_data.damage_name.split('-')[1] if '-' in report_data.damage_name else report_data.damage_name
        
        # DamageListに必要なフィールドを含むインスタンスを作成
        # << 損傷一覧(Excel)用データ登録 >>
        damage_list_entry = DamageList(
            parts_name = part.parts_name, # 主桁
            symbol = part.symbol, # Mg
            number = part.number, # 0101
            material = damage_list_materials[:-1], # 最後のコンマが不要なため[-1:]（S,C）
            main_parts = "〇" if part.main_frame else "", # 主要部材のフラグ
            damage_name = damage_name, # 剥離・鉄筋露出
            damage_lank = damage_lank, # d
            span_number = part.span_number,
            infra = part.infra
        )

        try:
            damage_list_entry.save()
            
        except IntegrityError:
            print("データが存在しています。")
            

"""所見用のクラス登録"""            
for part in parts_data:
    part_full_name = f"{part.parts_name} {part.symbol}{part.number}"
    span_number = part.span_number + '径間'

    # FullReportDataから部材名(主桁 Mg0101)、径間名、橋名が一致するデータを取得
    report_data_list = FullReportData.objects.filter(
        parts_name=part_full_name,
        span_number=span_number,
        infra=part.infra
    )
    # 全損傷から各損傷に分解(forループ)
    for report_data in report_data_list:        
        # 4桁の番号を2桁に変換
        main_parts_list_left = ["主桁", "PC定着部"] # 左の数字
        main_parts_list_right = ["横桁", "橋台"] # 右の数字
        main_parts_list_zero = ["床版"] # 00になる場合
        
        parts_name = f"{part.parts_name} {part.number}"
        
        if any(word in parts_name for word in main_parts_list_left):
            left = parts_name.find(" ")
            number2 = parts_name[left+1:]
            number_part = re.search(r'[A-Za-z]*(\d+)', number2).group(1)
            result_parts_name = parts_name[:left]+" "+number_part[:2] # 主桁 03
        elif any(word in parts_name for word in main_parts_list_right):
            right = parts_name.find(" ")
            number2 = parts_name[right+1:]
            number_part = re.search(r'[A-Za-z]*(\d+)', number2).group(1)
            if len(number_part) < 5:
                result_parts_name = parts_name[:right]+" "+number_part[2:] # 横桁 02
            else:
                result_parts_name = parts_name[:right]+" "+number_part[2:] # 横桁 103
        elif any(word in parts_name for word in main_parts_list_zero):
            right = parts_name.find(" ")
            result_parts_name = parts_name[:right]+" 00"
        else:
            right = parts_name.find(" ")
            result_parts_name = parts_name[:right]
            
        # 対象材料を取得し、記号に置換    
        damage_comment_material = ""
        for m in part.material.all():
            damage_comment_material += m.材料 + ","
        elements = damage_comment_material.split(',')
        replaced_elements = [material_replace_map.get(element, element) for element in elements] # それぞれの要素を置換辞書に基づいて変換
        damage_comment_materials = ','.join(replaced_elements) # カンマで結合

        # << 所見ページ用データ登録 >>
        damage_comment_entry = DamageComment(
            parts_name = result_parts_name, # 主桁 01
            material = damage_comment_materials[:-1], # S,C
            main_parts = "〇" if part.main_frame else "", # 主要部材のフラグ
            damage_name = damage_name,
            damage_max_lank = '', # e
            damage_min_lank = '', # b
            this_time_picture = report_data.this_time_picture,
            span_number = part.span_number,
            infra = part.infra
        )

        try:
            # DamageListインスタンスを保存
            damage_comment_entry.save()
            
        except IntegrityError:
            # 重複データがある場合の処理
            print("データが存在しています。")
            # 必要に応じてログを記録したり、他の処理を追加したりできます
            continue  # 次のループに進む