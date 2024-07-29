# <<正規表現で4桁以上の番号を取得>>
import re

def extract_number(text):
    # 正規表現パターン：4文字以上の連続する数字
    pattern = r'\d{4,}'
    # 正規表現検索によるマッチング
    matches = re.findall(pattern, text)
    return matches

names = [['主桁 Mg0101～0103'], ['沓座モルタル Bm0101']]

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

print(split_names)