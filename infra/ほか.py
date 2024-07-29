import re

def extract_number(text):
    """
    テキストから4文字以上の連続する数字を抽出する関数。
    """
    pattern = r'\d{4,}'
    matches = re.findall(pattern, text)
    return matches

names = '防護柵 Mg0101'

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
        
print(split_number)
result = parts_join + split_number
print(result)