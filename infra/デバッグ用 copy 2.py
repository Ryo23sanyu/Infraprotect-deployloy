import re


items = [{'first': '排水管 Dp0101', 'second': ['①腐食(大大)-e', '⑤防食機能の劣化(分類1)-e'], 'third': '写真番号-31', 'last': ['infra/img\\9月7日\\u3000佐藤\\u3000地上\\P9070422.JPG'], 'picture': 'infra/noImage.png'}, {'first': '主桁 Mg0302', 'second': ['⑦剥離・鉄筋露出-d'], 'third': '写真番号-5', 'last': ['infra/img\\9月7日\\u3000佐藤\\u3000地上\\P9070503.JPG'], 'picture': 'infra/noImage.png'}]

# 抽出・置換ロジックをここに実装

# bridge.secondをどのように置換するかのロジック
replacement_patterns = {
    "①腐食(大大)-e": "板厚減少を伴う腐食",
    "⑦剥離・鉄筋露出-c": "コンクリートの剥離",
    "⑦剥離・鉄筋露出-d": "鉄筋露出",
    "⑦剥離・鉄筋露出-e": "著しい鉄筋露出",
    "⑳漏水・滞水-e": "著しい鉄筋露出",
}
 
second_items = [item['second'] for item in items]

# 第一のロジックを各サブリストに対して実行
for i, sublist in enumerate(second_items):
    if any(item.startswith('①') for item in sublist):
        sublist[:] = [item for item in sublist if not item.startswith('⑤')]

    # 正規表現を使い、特定の文字列を処理する
    new_sublist = []
    for item in sublist:
        if item.startswith('⑰'):
            match = re.search(r':(.*?)(?=\)-e)', item)
            if match:
                new_sublist.append(match.group(1))
            else:
                new_sublist.append(item)
        else:
            new_sublist.append(item)
    second_items[i][:] = new_sublist

# 二次の置換ロジックと出力（例示目的のダミーコードを含む）
# `replacement_patterns`及び出力処理が未定義であるため、この部分は省略または修正が必要です。

# 以下は単純な出力例
for item in items:
    modified_first_item = item['first'][:item['first'].find(" ")] if " " in item['first'] else item['first']
    second_replaced = "、".join(replacement_patterns.get(s_item, s_item) for s_item in item['second'])
    print(f"{modified_first_item}に{second_replaced}が見られる。")
