first_and_second = []

bridge_damage = [{'first': [['主桁 Mg0101～0204', '主桁 Mg0302', '主桁 Mg0304', '主桁 Mg0401～0403']], 'second': [['⑦剥離・鉄筋露出-d']]}]

for first_buzai_item in bridge_damage:
    #print(item)
    first_elements = first_buzai_item['first'][0]  # ['床版 Ds0201', '床版 Ds0203']
    second_elements = first_buzai_item['second'][0]  # ['⑦剥離・鉄筋露出-d']

    
    # first の要素と second を一対一で紐付け
    for first_buzai_second_name in first_elements:
        first_and_second.append({'first': [first_buzai_second_name], 'second': second_elements})
print(first_and_second)