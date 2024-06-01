import re


text = {'first': [['主桁 Mg0101～0203']], 'second': [['⑦剥離・鉄筋露出-c']], 'join': [{'first': ['主桁 Mg0901'], 'second': ['⑦剥離・鉄筋露出-c']}], 'third': '写真番号-1', 'last': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070537.JPG'], 'picture': 'infra/noImage.png', 'textarea_content': '主桁にコンクリートの剥離が見られる。', 'damage_coordinate': ['528508.2182060345', '218366.5575399188'], 'picture_coordinate': ['529225.1221130126', '218048.3941777406']}

first_step = text['first'][0][0] # firstキーの最初の要素
print(first_step) # 主桁 Mg0101～0203

if " " in first_step:
    # 部材記号の前にスペースが「含まれている」場合
    first_step_split = first_step.split()
    print(first_step_split) # ['主桁', 'Mg0101～0203']
else:
    # 部材記号の前にスペースが「含まれていない」場合
    first_step_split = re.split(r'(?<=[^a-zA-Z])(?=[a-zA-Z])', first_step) # アルファベット以外とアルファベットの並びで分割
    first_step_split = [kara for kara in first_step_split if kara] # re.split()の結果には空文字が含まれるので、それを取り除く
    print(first_step_split) # ['主桁', 'Mg0101～0203']

# 正規表現
number = first_step_split[1]
print(number) # 'Mg0101～0203'
# マッチオブジェクトを取得

# マッチオブジェクトを取得
number_part = re.search(r'[A-Za-z]*(\d+～\d+)', number).group(1)
print(number_part) # '0101～0203'

one = number_part.find("～")

start_number = number_part[:one]
print(start_number) # 0101
end_number = number_part[one+1:]
print(end_number) # 0203

# 最初の2桁と最後の2桁を取得
start_prefix = start_number[:2]
start_suffix = start_number[2:]
end_prefix = end_number[:2]
end_suffix = end_number[2:]

number_arrangement = ""
for prefix in range(int(start_prefix), int(end_prefix)+1):
    for suffix in range(int(start_suffix), int(end_suffix)+1):
        number_arrangement += "{:02d}{:02d}\n".format(prefix, suffix)
        
print(number_arrangement)