damage_data = {'parts_name': [['主桁 Mg0901']], 'damage_name': [['⑦剥離・鉄筋露出-c']], 'join': [{'parts_name': ['主桁 Mg0901'], 'damage_name': ['⑦剥離・鉄筋露出-c']}], 'picture_number': '写真番号-1', 'this_time_picture': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070537.JPG'], 'last_time_picture': None, 'textarea_content': '主桁にコンクリー トの剥離が見られる。', 'damage_coordinate': ['528508.2182060345', '218366.5575399188'], 'picture_coordinate': ['529225.1221130126', '218048.3941777406'], 'search': '1径間'}

# ['528508.2182060345', '218366.5575399188']
print(float(damage_data['damage_coordinate'][0]))
print(float(damage_data['damage_coordinate'][1]))