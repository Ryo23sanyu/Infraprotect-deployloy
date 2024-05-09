import re


second_items = [['⑦剥離・鉄筋露出-d'], ['⑰その他(分類6:異物混入)-e']]

replacement_patterns = {
    "①腐食(大大)-e": "板厚減少を伴う腐食",
    "⑦剥離・鉄筋露出-c": "コンクリートの剥離",
    "⑦剥離・鉄筋露出-d": "鉄筋露出",
    "⑦剥離・鉄筋露出-e": "著しい鉄筋露出",
    "⑳漏水・滞水-e": "著しい鉄筋露出",
}
    
# << ①と⑤があるとき、⑤を消す >>
for sublist in second_items:
# リスト内の要素を走査して、先頭が「①」の要素が存在するかチェックする
    if any(item.startswith('①') for item in sublist):
        # 「①」で始まる要素があれば、「⑤」で始まる要素を全て削除
        # サブリストのコピー上でイテレーションを行いながら、元のサブリストを編集
        sublist[:] = [item for item in sublist if not item.startswith('⑤')]
        
    # << ⑰のとき、「⑰その他(分類6:)-e」を消す >>    
    new_sublist = []  # sublistを更新するための一時リスト
    for item in sublist:
        if item.startswith('⑰'):
            # 正規表現を使って「:」から「)-e」までの文字列を抽出する
            match = re.search(r':(.*?)(?=\)-e)', item)
            if match:
                # 抽出した部分をsublistに追加
                new_sublist.append(match.group(1))
        else:
            new_sublist.append(item)
    sublist[:] = new_sublist

    second_replaced = "、".join(replacement_patterns.get(char, char) for char in sublist)
    print(second_replaced)