import re

pattern = r"⑰.*?\(.*?:(.*?)\)-e"
item = "⑰その他(分類6:抽出したい文字列)-e"
match = re.search(pattern, item)

if match:
    print("抽出結果:", match.group(1))
else:
    print("マッチしませんでした")
