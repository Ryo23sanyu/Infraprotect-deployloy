text = [['①-e', '⑤-e'], ['①-e', '⑤-e']]

# 全てのサブリストに対して処理をする
for sublist in text:
    # サブリスト内に「①」で始まる要素があるかチェック
    if any(item.startswith('①') for item in sublist):
        # 「①」で始まる要素があれば、「⑤」で始まる要素を全て削除
        # サブリストのコピー上でイテレーションを行いながら、元のサブリストを編集
        sublist[:] = [item for item in sublist if not item.startswith('⑤')]

print(text) 

import re

# 指定されたリスト
texts = ['⑤防食機能の劣化(分類1)-e', '⑰その他(分類6:破壊)-e']

# 抽出されたテキストを格納するためのリスト
extracted_texts = []

# リスト内の各テキストに対して処理
for text in texts:
    # テキストの先頭が⑰である場合のみ処理を行う
    if text.startswith('⑰'):
        # 正規表現を使って「:」から「)-e」の直前まで（「)」は含まない）の文字列を抽出する
        match = re.search(r':(.*?)(?=\)-e)', text)
        if match:
            # 抽出した部分をリストに追加
            extracted_texts.append(match.group(1))

# 結果を表示
print(extracted_texts)