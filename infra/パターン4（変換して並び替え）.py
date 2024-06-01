import re


damage_table = [{'first': [['横桁 Cr0803']], 'second': [['⑦剥離・鉄筋露出-d']], 'join': [{'first': ['横桁 Cr0803'], 'second': ['⑦剥離・鉄筋露出-d']}], 'third': '写真番号-15', 'last': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070458.JPG'], 'picture': 'infra/noImage.png', 'textarea_content': '横桁に鉄筋露出が見られる。', 'damage_coordinate': ['543207.0862507953', '218366.5575399188'], 'picture_coordinate': ['545418.5774821687', '218368.3759352968']},\
    {'first': [['主桁 Mg0901']], 'second': [['⑰その他(分類6:異物混入)-e']], 'join': [{'first': ['主桁 Mg0901'], 'second': ['⑰その他(分類6:異物混入)-e']}], 'third': '写真番号-2', 'last': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070404.JPG'], 'picture': 'infra/noImage.png', 'textarea_content': '主桁に異物混入が見られる。', 'damage_coordinate': ['532240.3861927793', '218366.5575399188'], 'picture_coordinate': ['534192.8564975171', '218396.3930096343']}, \
        {'first': [['横桁 Cr0503']], 'second': [['⑦剥離・鉄筋露出-d', '⑰その他(分類6:施工不良)-e']], 'join': [{'first': ['横桁 Cr0503'], 'second': ['⑦剥離・鉄筋露出-d', '⑰その他(分類6:施工不良)-e']}], 'third': '写真番号-10,11', 'last': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070450.JPG', 'infra/img\\9月7日\u3000佐藤\u3000地上\\P9070452.JPG'], 'picture': 'infra/noImage.png', 'textarea_content': '横桁に鉄筋露出,施工不良が見られる。 \n【関連損傷】\n横桁 Cr0503:⑰その他(分類6:施工不良)-e', 'damage_coordinate': ['546181.340571892', '222553.0807470059'], 'picture_coordinate': ['546769.9402349197', '222164.8389810835']}, \
            {'first': [['主桁 Mg0901']], 'second': [['⑦剥離・鉄筋露出-c']], 'join': [{'first': ['主桁 Mg0901'], 'second': ['⑦剥離・鉄筋露出-c']}], 'third': '写真番号-1', 'last': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070537.JPG'], 'picture': 'infra/noImage.png', 'textarea_content': '主桁にコンクリートの剥離が見られる。', 'damage_coordinate': ['528508.2182060345', '218366.5575399188'], 'picture_coordinate': ['529225.1221130126', '218048.3941777406']}, \
                {'first': [['地覆 Fg0201']], 'second': [['⑫うき-e']], 'join': [{'first': ['地覆 Fg0201'], 'second': ['⑫うき-e']}], 'third': '写真番号-24', 'last': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070535.JPG'], 'picture': 'infra/noImage.png', 'textarea_content': '地覆にコンクリートのうきが見られる。', 'damage_coordinate': ['529523.5331537114', '216164.654853505'], 'picture_coordinate': ['529841.2180579801', '215806.1718362219']}, {'first': [['橋台[胸壁] Ap0102', '橋台[竪壁] Ac0102', '伸縮装置 Ej0102']], 'second': [['⑳漏水・滞水-e']], 'join': [{'first': ['橋台[胸壁] Ap0102'], 'second': ['⑳漏水・滞水-e']}, {'first': ['橋台[竪壁] Ac0102'], 'second': ['⑳漏水・滞水-e']}, {'first': ['伸縮装置 Ej0102'], 'second': ['⑳漏水・滞水-e']}], 'third': '写真番号-19', 'last': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070443.JPG'], 'picture': 'infra/noImage.png', 'textarea_content': '橋台[胸壁]および橋台[竪壁],伸縮装置に漏水・滞水が見られる。 \n【関連損傷】\n橋台[竪壁] Ac0102,伸縮装置 Ej0102:⑳漏水・滞水-e', 'damage_coordinate': ['534633.1754138757', '198400.9331532792'], 'picture_coordinate': ['537045.4396522791', '198420.7293499758']}, \
                    {'first': [['橋台[胸壁] Ap0101', '橋台[竪壁] Ac0101', '伸縮装置 Ej0101']], 'second': [['⑳漏水・滞水-e']], 'join': [{'first': ['橋台[胸壁] Ap0101'], 'second': ['⑳漏水・滞水-e']}, {'first': ['橋台[竪壁] Ac0101'], 'second': ['⑳漏水・滞水-e']}, {'first': ['伸縮装置 Ej0101'], 'second': ['⑳漏水・滞水-e']}], 'third': '写真番号-18', 'last': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070438.JPG'], 'picture': 'infra/noImage.png', 'textarea_content': '橋台[胸壁]および橋台[竪壁],伸縮装置に漏水・滞水が見られる。 \n【関連損傷】\n橋台[竪壁] Ac0101,伸縮装置 Ej0101:⑳漏水・滞水-e', 'damage_coordinate': ['535305.6406762057', '190342.4721676922'], 'picture_coordinate': ['537494.8440878117', '190371.7813098583']}, \
                    {'first': [['防護柵 Gf0101']], 'second': [['⑦剥離・鉄筋露出-d']], 'join': [{'first': ['防護柵 Gf0101'], 'second': ['⑦剥離・鉄筋露出-d']}], 'third': '写真番号-22', 'last': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070620.JPG'], 'picture': 'infra/noImage.png', 'textarea_content': '防護柵に鉄筋露出が見られる。', 'damage_coordinate': ['538818.4080393101', '169468.5013850681'], 'picture_coordinate': ['539306.9846939673', '169153.6834979908']}, \
                        {'first': [['舗装 Pm0101']], 'second': [['㉔土砂詰まり-e']], 'join': [{'first': ['舗装 Pm0101'], 'second': ['㉔土砂詰まり-e']}], 'third': '写真番号-26', 'last': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070596.JPG'], 'picture': 'infra/noImage.png', 'textarea_content': '舗装に土砂詰まりが見られる。', 'damage_coordinate': ['533352.4944797055', '168103.8976152274'], 'picture_coordinate': ['533703.9706752875', '167792.7034569031']}, \
                       {'first': [['PC定着部 Cn1203']], 'second': [['NON-a']], 'join': [{'first': ['PC定着部 Cn1203'], 'second': ['NON-a']}], 'third': None, 'last': None, 'picture': 'infra/noImage.png', 'textarea_content': 'PC定着部にNON-aが見られる。', 'damage_coordinate': ['530448.4275586283', '165439.1406174743'], 'picture_coordinate': None}, \
                           {'first': [['排水ます Dr0102', '排水ます Dr0201', '排水ます Dr0202']], 'second': [['⑰その他(分類6:埋没)-e']], 'join': [{'first': ['排水ます Dr0102'], 'second': ['⑰その他(分類6:埋没)-e']}, {'first': ['排水ます Dr0201'], 'second': ['⑰その他(分類6:埋没)-e']}, {'first': ['排水ます Dr0202'], 'second': ['⑰その他(分類6:埋没)-e']}], 'third': None, 'last': None, 'picture': 'infra/noImage.png', 'textarea_content': '排水ますに埋没が見られる。 \n【関連損傷】\n排水ます Dr0201,排水ます Dr0202:⑰その他(分類6:埋没)-e', 'damage_coordinate': ['525003.839727268', '156577.5780402338'], 'picture_coordinate': None}]


#優先順位の指定
order_dict = {"主桁": 1, "横桁": 2, "床版": 3, "PC定着部": 4, "橋台[胸壁]": 5, "橋台[竪壁]": 6, "支承本体": 7, "沓座モルタル": 8, "防護柵": 9, "地覆": 10, "伸縮装置": 11, "舗装": 12, "排水ます": 13, "排水管": 14}
order_number = {"None": 0, "①": 1, "②": 2, "③": 3, "④": 4, "⑤": 5, "⑥": 6, "⑦": 7, "⑧": 8, "⑨": 9, "⑩": 10, "⑪": 11, "⑫": 12, "⑬": 13, "⑭": 14, "⑮": 15, "⑯": 16, "⑰": 17, "⑱": 18, "⑲": 19, "⑳": 20, "㉑": 21, "㉒": 22, "㉓": 23, "㉔": 24, "㉕": 25, "㉖": 26}
order_lank = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
        
# <<◆ リストの並び替え ◆>>
def sort_key_function(sort_item):
    first_value = sort_item['first'][0][0] # firstキーの最初の要素
    #print(first_value) # 主桁 Mg0901

    if " " in first_value:
        # 部材記号の前にスペースが「含まれている」場合
        first_value_split = first_value.split()
        #print(first_value_split) # ['主桁', 'Mg0901']
    else:
        # 部材記号の前にスペースが「含まれていない」場合
        first_value_split = re.split(r'(?<=[^a-zA-Z])(?=[a-zA-Z])', first_value) # アルファベット以外とアルファベットの並びで分割
        first_value_split = [x for x in first_value_split if x] # re.split()の結果には空文字が含まれるので、それを取り除く
        #print(first_value_split) # ['主桁', 'Mg0901']

    first_name_key = order_dict.get(first_value_split[0], float('inf'))
    #print(first_name_key) # 1

    first_number_key = int(first_value_split[1][2:])
    #print(first_number_key) # 901

    if sort_item['second'][0][0]:  # `second`キーが存在する場合
        second_value = sort_item['second'][0][0] # secondキーの最初の要素
        #print(second_value) # ⑰その他(分類6:異物混入)-e
        second_number_key = order_number.get(second_value[0], float('inf'))  # 先頭の文字を取得してorder_numberに照らし合わせる
        #print(second_number_key) # 17
        second_lank_key = order_lank.get(second_value[-1], float('inf'))  # 末尾の文字を取得してorder_lankに照らし合わせる
        #print(second_lank_key) # 5
    else:
        second_number_key = float('inf')
        second_lank_key = float('inf')
            
    return (first_name_key, first_number_key, second_number_key, second_lank_key)

sorted_items = sorted(damage_table, key=sort_key_function)

# ソート結果を表示
for item in sorted_items:
    print(item)