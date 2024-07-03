import re


first_and_second = []

bridge_damage = [{'first': ['主桁 Mg(0101～0204):S,C/●', '主桁 Mg(0302):S,C/●', '主桁 Mg(0304):S,C/●', '主桁 Mg(0401～0403):S,C/●']}]

for first_buzai_item in bridge_damage:
    first_elements = first_buzai_item['first'][0] # 主桁 Mg(0101～0204):S,C/●
    print(first_elements)
    
    # first の要素と second を一対一で紐付け
    if "～" in first_elements:

        first_part = first_elements.split('(')[0] # 主桁 Mg
        number_part = first_elements.split('(')[1].split(')')[0] # 0101～0204
        remaining_part = first_elements.split(')')[1] # :S,C/●

        one = number_part.find("～")

        start_number = number_part[:one] # 0101
        end_number = number_part[one+1:] # 0204

        # 最初の2桁と最後の2桁を取得
        start_prefix = start_number[:2] # 01
        start_suffix = start_number[2:] # 01
        end_prefix = end_number[:2] # 02
        end_suffix = end_number[2:] # 04
                
        number_arrangement = []
        for prefix in range(int(start_prefix), int(end_prefix)+1):
            for suffix in range(int(start_suffix), int(end_suffix)+1):
                number_items = "{:02d}{:02d}".format(prefix, suffix)
                join_item = first_part + "(" + number_items + ")" + remaining_part
                number_arrangement.append(join_item)
        print(number_arrangement)