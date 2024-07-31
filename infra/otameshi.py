def join_to_result_string(join):
    result_parts = []
    for item in join:
        parts_name = item['parts_name'][0]
        damage_names = item['damage_name']
        formatted_damage_names = '/'.join(damage_names)
        result_parts.append(f"{parts_name} : {formatted_damage_names}")
    return ', '.join(result_parts)

database_sorted_items = {'parts_name': [['主桁 Mg0101～0204', '主桁 Mg0302', '主桁 Mg0304', '主桁 Mg0401～0403']], 'damage_name': [['⑦剥離・鉄筋露出-d']], 
                         'join': [{'parts_name': ['主桁 Mg0101'], 'damage_name': ['⑦剥離・鉄筋露出-d']}, {'parts_name': ['主桁 Mg0102'], 'damage_name': ['⑦剥離・鉄筋露出-d']}, 
                                  {'parts_name': ['主桁 Mg0103'], 'damage_name': ['⑦剥離・鉄筋露出-d']}, {'parts_name': ['主桁 Mg0104'], 'damage_name': ['⑦剥離・鉄筋露出-d']}, 
                                  {'parts_name': ['主桁 Mg0201'], 'damage_name': ['⑦剥離・鉄筋露出-d']}, {'parts_name': ['主桁 Mg0202'], 'damage_name': ['⑦剥離・鉄筋露出-d']}, 
                                  {'parts_name': ['主桁 Mg0203'], 'damage_name': ['⑦剥離・鉄筋露出-d']}, {'parts_name': ['主桁 Mg0204'], 'damage_name': ['⑦剥離・鉄筋露出-d']}, 
                                  {'parts_name': ['主桁 Mg0302'], 'damage_name': ['⑦剥離・鉄筋露出-d']}, {'parts_name': ['主桁 Mg0304'], 'damage_name': ['⑦剥離・鉄筋露出-d']}, 
                                  {'parts_name': ['主桁 Mg0401'], 'damage_name': ['⑦剥離・鉄筋露出-d']}, {'parts_name': ['主桁 Mg0402'], 'damage_name': ['⑦剥離・鉄筋露出-d']}, 
                                  {'parts_name': ['主桁 Mg0403'], 'damage_name': ['⑦剥離・鉄筋露出-d']}], 'picture_number': None, 'this_time_picture': None, 'last_time_picture': None, 
                         'textarea_content': '主桁に鉄筋露出が見られる。 \n【関連損傷】\n主桁 Mg0302,主桁 Mg0304,主桁 Mg0401～0403:⑦剥離・鉄筋露出-d', 
                         'damage_coordinate': ['525003.839727268', '213095.7270112425'], 'picture_coordinate': None, 'search': '1径間'}


if not is_multi_list(split_names) and not is_multi_list(damages) and name_length == 1:
    for single_damage in damages: 
        parts_name = names[0]
        damage_name = flatten(single_damage)

elif not is_multi_list(split_names) and not is_multi_list(damages) and name_length >= 2:
    if damage_length == 1:
        for single_name in split_names:
            parts_name = single_name
            damage_name = flatten(damages[0])

    elif not is_multi_list(split_names) and not is_multi_list(damages) and damage_length >= 2:
        for name in split_names:
            for damage in damages:
                parts_name = name
                damage_name = flatten(damage)

else:
    for i in range(name_length):
        for name in split_names[i]:
            for damage in damages[i]:
                parts_name = name
                damage_name = flatten(damage)
                
data_fields = {
    'parts_name': names,
    'damage_name': damages,
    'damage_coordinate_x': damage_coordinate_x,
    'damage_coordinate_y': damage_coordinate_y,
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