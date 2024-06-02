import re


first_and_second = []

bridge_damage = [{'first': [['主桁 Mg0101～0204', '主桁 Mg0302', '主桁 Mg0304', '主桁 Mg0401～0403']], 'second': [['⑦剥離・鉄筋露出-d']]}]

for first_buzai_item in bridge_damage:
    #print(item)
    first_elements = first_buzai_item['first'][0]  # ['床版 Ds0201', '床版 Ds0203']
    second_elements = first_buzai_item['second'][0]  # ['⑦剥離・鉄筋露出-d']

    
    # first の要素と second を一対一で紐付け
    for first_buzai_second_name in first_elements:
        if "～" in first_buzai_second_name:

            first_step = first_buzai_second_name

            if " " in first_step:
                # 部材記号の前にスペースが「含まれている」場合
                first_step_split = first_step.split()

            else:
                # 部材記号の前にスペースが「含まれていない」場合
                first_step_split = re.split(r'(?<=[^a-zA-Z])(?=[a-zA-Z])', first_step) # アルファベット以外とアルファベットの並びで分割
                first_step_split = [kara for kara in first_step_split if kara] # re.split()の結果には空文字が含まれるので、それを取り除く

            # 正規表現
            number = first_step_split[1]
            # マッチオブジェクトを取得

            # マッチオブジェクトを取得
            number_part = re.search(r'[A-Za-z]*(\d+～\d+)', number).group(1)

            one = number_part.find("～")

            start_number = number_part[:one]
            end_number = number_part[one+1:]

            # 最初の2桁と最後の2桁を取得
            start_prefix = start_number[:2]
            start_suffix = start_number[2:]
            end_prefix = end_number[:2]
            end_suffix = end_number[2:]

            # 「主桁 Mg」を抽出
            prefix_text = first_step_split[0] + " " + re.match(r'[A-Za-z]+', number).group(0)

            number_arrangement = []
            for prefix in range(int(start_prefix), int(end_prefix)+1):
                for suffix in range(int(start_suffix), int(end_suffix)+1):
                    number_items = "{}{:02d}{:02d}".format(prefix_text, prefix, suffix)
                    first_and_second = {'first': [number_items], 'second': second_elements}
                    print([first_and_second])
        else:
            first_and_second = {'first': [first_buzai_second_name], 'second': second_elements}
            print([first_and_second])