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
        
# print(split_number)
result = parts_join + split_number
# print(result)

text = "アクション-1 Acn1150"

# 文字列を空白で分ける
parts = text.split()

# 最初の部分「アクション-1」を取得
part1 = parts[0]

# 2番目の部分から数値部分だけを取得
part2 = re.search(r'\d+', parts[1]).group()

print(part1)  # 出力: アクション-1
print(part2)  # 出力: 1150


# 文章
text = "①大当たり"

# 置き換え用の辞書
dictionary = {
    "①": "1等",
    "②": "2等"
}

# 先頭の1文字を取得
first_char = text[0]

# 辞書で値を取得
result = dictionary.get(first_char, "キーが見つかりません")

print(result)  # 出力: 1等

points = 546386.0254916904,168103.8976152274
print(points[0])

points = "546386.0254916904,168103.8976152274"
print(points[0])
# コンマで分割して、リストにする
left, right = points.split(',')

# 結果を表示
print(f"左側: {left}")
print(f"右側: {right}")

parts_name = "他21 another000101"

# 正規表現パターンを定義
pattern = r"(\d+)$"

# parts_nameからパターンにマッチする部分を検索
match = re.search(pattern, parts_name)

# マッチした場合にその部分を取得
if match:
    last_number = match.group(1)
    print("末尾の数字は:", last_number)
else:
    print("数字が見つかりませんでした")
