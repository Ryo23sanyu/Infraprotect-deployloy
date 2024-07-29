import re


damage_data = {'parts_name': [['主桁 Mg0901']], 'damage_name': [['⑦剥離・鉄筋露出-c']], 
               'join': [{'parts_name': ['主桁 Mg0901'], 'damage_name': ['⑦剥離・鉄筋露出-c']}], 
               'picture_number': '写真番号-1', 'this_time_picture': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070537.JPG'], 
               'last_time_picture': None, 'textarea_content': '主桁にコンクリートの剥離が見られる。', 
               'damage_coordinate': ['528508.2182060345', '218366.5575399188'], 
               'picture_coordinate': ['529225.1221130126', '218048.3941777406'], 'search': '1径間'}

damage_data = {'parts_name': [['支承本体 Bh0101'], ['沓座モルタル Bm0101']], 
               'damage_name': [['①腐食(小小)-b', '⑤防食機能の劣化(分類1)-e', '㉓変形・欠損-c'], ['⑦剥離・鉄筋露出-c']], 
               'join': [{'parts_name': ['支承本体 Bh0101'], 'damage_name': ['①腐食(小小)-b', '⑤防食機能の劣化(分類1)-e', '㉓変形・欠損-c']}, {'parts_name': ['沓座モルタル Bm0101'], 'damage_name': ['⑦剥離・鉄筋露出-c']}], 
               'picture_number': '写真番号-27', 'this_time_picture': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070504.JPG'], 
               'last_time_picture': None, 'textarea_content': '支承本体に腐食,変形・欠損が見られる。また沓座モルタルにコンクリートの剥離が見られる。 \n【関連損傷】\n支承本体 Bh0101:㉓変形・欠損-c, 沓座モルタル Bm0101:⑦剥離・鉄筋露出-c', 
               'damage_coordinate': ['589100.6408404222', '223935.3885015437'], 'picture_coordinate': ['591543.5416080136', '223659.8990548863'], 
               'search': '2径間'}


def flatten(value):
    def _flatten(nested_list):
        if isinstance(nested_list, list):
            for item in nested_list:
                yield from _flatten(item)
        else:
            yield nested_list
    
    return ', '.join(_flatten(value))

# <<正規表現で4桁以上の番号を取得>>
def extract_number(text):
    # 正規表現パターン：4文字以上の連続する数字
    pattern = r'\d{4,}'
    # 正規表現検索によるマッチング
    matches = re.findall(pattern, text)
    return matches

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

split_items = []

for item in names:
    for split in item:
        if "～" in split:
            one = split.find("～")
            start_number = ''.join(extract_number(split[:one])) # 0101
            end_number = split[one+1:] # 0204

            # 最初の2桁と最後の2桁を取得
            start_prefix = start_number[:2] # 01
            start_suffix = start_number[2:] # 01
            end_prefix = end_number[:2] # 02
            end_suffix = end_number[2:] # 04
            
            part_name = split[:one].replace(start_number, '')
        
            for prefix in range(int(start_prefix), int(end_prefix)+1):
                for suffix in range(int(start_suffix), int(end_suffix)+1):
                    number_items = "{:02d}{:02d}".format(prefix, suffix)
                    join_item = part_name + number_items
                    split_items.append(join_item)
            
        else:
            split_items.append(split)

split_names = []
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
    """
    与えられたnamesを処理し、適切な部分を返す関数。
    """
    
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


if not is_multi_list(split_names) and not is_multi_list(damages) and name_length == 1: # 部材名が1つの場合
    for single_damage in damages: 
        parts_name = names[0]
        damage_name = flatten(single_damage)
        parts_split = process_names(flatten(parts_name))
        
        parts_name = parts_name
        damage_name = damage_name
        parts_split = parts_split
        join = join
        picture_number = numbers_only
        this_time_picture = this_time_picture
        last_time_picture = last_time_picture
        textarea_content = textarea_content
        damage_coordinate_x = damage_coordinate_x
        damage_coordinate_y = damage_coordinate_y
        picture_coordinate_x = picture_coordinate_x
        picture_coordinate_y = picture_coordinate_y
        span_number = span_number
        special_links = '/'.join([str(parts_split), str(damage_name), str(span_number)])

elif not is_multi_list(split_names) and not is_multi_list(damages) and name_length >= 2: # 部材名が2つ以上の場合
    if damage_length == 1: # かつ損傷名が1つの場合
        for single_name in split_names:
            parts_name = single_name
            damage_name = flatten(damages[0])
            parts_split = process_names(flatten(parts_name))

            parts_name = parts_name
            damage_name = damage_name
            parts_split = parts_split
            join = join
            picture_number = numbers_only
            this_time_picture = this_time_picture
            last_time_picture = last_time_picture
            textarea_content = textarea_content
            damage_coordinate_x = damage_coordinate_x
            damage_coordinate_y = damage_coordinate_y
            picture_coordinate_x = picture_coordinate_x
            picture_coordinate_y = picture_coordinate_y
            span_number = span_number
            special_links = '/'.join([str(parts_split), str(damage_name), str(span_number)])

    elif not is_multi_list(split_names) and not is_multi_list(damages) and damage_length >= 2: # かつ損傷名が2つ以上の場合
        for name in split_names:
            for damage in damages:
                parts_name = name
                damage_name = flatten(damage)
                parts_split = process_names(flatten(parts_name))

                parts_name = parts_name
                damage_name = damage_name
                parts_split = parts_split
                join = join
                picture_number = numbers_only
                this_time_picture = this_time_picture
                last_time_picture = last_time_picture
                textarea_content = textarea_content
                damage_coordinate_x = damage_coordinate_x
                damage_coordinate_y = damage_coordinate_y
                picture_coordinate_x = picture_coordinate_x
                picture_coordinate_y = picture_coordinate_y
                span_number = span_number
                special_links = '/'.join([str(parts_split), str(damage_name), str(span_number)])


else: # 多重リストの場合
    for i in range(name_length):
        for name in split_names[i]:
            for damage in damages[i]:
                parts_name = name
                damage_name = flatten(damage)
                parts_split = process_names(flatten(parts_name))

                parts_name = parts_name
                damage_name = damage_name
                parts_split = parts_split
                join = join
                picture_number = numbers_only
                this_time_picture = this_time_picture
                last_time_picture = last_time_picture
                textarea_content = textarea_content
                damage_coordinate_x = damage_coordinate_x
                damage_coordinate_y = damage_coordinate_y
                picture_coordinate_x = picture_coordinate_x
                picture_coordinate_y = picture_coordinate_y
                span_number = span_number
                special_links = '/'.join([str(parts_split), str(damage_name), str(span_number)])

print(parts_name)
print(damage_name)
print(parts_split)
print(join)
print(picture_number)
print(this_time_picture)
print(last_time_picture)
print(textarea_content)
print(damage_coordinate_x)
print(damage_coordinate_y)
print(picture_coordinate_x)
print(picture_coordinate_y)
print(span_number)
print(special_links)