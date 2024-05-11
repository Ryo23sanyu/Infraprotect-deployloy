import re

# 元の文字列
text = "種 Ta0101,0205,葉 Ha0808"

# アルファベット、数字、コンマを除去し日本語のみを抽出するための正規表現パターン
pattern = r'[A-Za-z0-9,]'

# 置換処理を行い、日本語のみ抽出
result = re.sub(pattern, '', text)

print(result)  # 出力：種 葉