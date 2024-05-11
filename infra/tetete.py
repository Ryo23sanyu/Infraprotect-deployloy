import re
from markupsafe import Markup

item = {'first': Markup('横桁 Cr0803'), 'second': ['⑦剥離・鉄筋露出-d'], 'third': '写真番号-15', 'last': ['infra/img\\9月7日\u3000佐藤\u3000地上\\P9070458.JPG'], 'picture': 'infra/noImage.png'}

bridge = {
    "first": Markup('横桁 Cr0803'),
    "second": ['⑦剥離・鉄筋露出-d']
}

# bridge.secondを置換する辞書
replacement_patterns = {
    "①腐食(小小)-b": "腐食",
    "①腐食(小大)-c": "拡がりのある腐食",
    "①腐食(大小)-d": "板厚減少を伴う腐食",
    "①腐食(大大)-e": "板厚減少を伴う拡がりのある腐食",
    "③ゆるみ・脱落-c": "ボルトのゆるみ・脱落(〇本中〇本)",
    "③ゆるみ・脱落-e": "ボルトのゆるみ・脱落(〇本中〇本)",
    "④破断-e": "破断",
    "⑦剥離・鉄筋露出-c": "コンクリートの剥離",
    "⑦剥離・鉄筋露出-d": "鉄筋露出",
    "⑦剥離・鉄筋露出-e": "著しい鉄筋露出",
    "⑨抜け落ち-e": "コンクリート塊の抜け落ち",
    "⑫うき-e": "コンクリートのうき",
    "⑮舗装の異常-c": "最大幅0.0mmのひびわれ",
    "⑮舗装の異常-e": "最大幅0.0mmのひびわれ・舗装の土砂化",
    "⑳漏水・滞水-e": "漏水・滞水",
    "㉑異常な音・振動-e": "異常な音・振動",
    "㉒異常なたわみ-e": "異常なたわみ",
    "㉓変形・欠損-c": "変形・欠損",
    "㉓変形・欠損-e": "著しい変形・欠損",
    "㉔土砂詰まり-e": "土砂詰まり",
    "㉕沈下・移動・傾斜-e": "移動量0.0mmの沈下・移動・傾斜",
}

    # << ①と⑤があるとき、⑤を消す >>
second_items = ['⑦剥離・鉄筋露出-d']
for sublist in second_items:# リスト内の要素を走査して、先頭が「①」の要素が存在するかチェックする
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
        else:
            new_sublist.append(item)
            
    sublist[:] = new_sublist


        # 抽出・置換ロジックをここに実装
first_part_extracted = bridge["first"][:bridge["first"].find(" ")]
#print(first_part_extracted)
#print(bridge["second"])
second_replaced = "、".join(replacement_patterns.get(char, char) for char in bridge["second"])
        # print(second_replaced)
print(first_part_extracted + "に" + second_replaced + "が見られる。")