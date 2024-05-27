from markupsafe import Markup


text_items = [Markup('床版 Ds0201,0203')]

# 一つずつループで処理
result_items = [] # 結果配列を作成
for item in text_items:
    if ',' in item:
        # カンマが含まれている場合カンマで分割
        sub_items = item.split(',')
        for i, sitem in enumerate(sub_items):
            # 二つ目以降、かつ１文字目が数字の場合
            if i > 0 and sitem[0].isnumeric():
                # カンマ区切りの一つ前の項目を取り出す
                before_sub_item = sub_items[i -1]
                # 取り出した文字列のスペースより前を取り出す
                before_sub_item_splited = before_sub_item.split()
                before_sub_item_before = before_sub_item_splited[0]
                # 取り出した文字列のスペースより後を取り出す
                before_sub_item_after = before_sub_item_splited[1]
                # 後半部分の数字より前部分を取り出す
                before_sub_item_after_prefix = ''
                for s in before_sub_item_after:
                    if s.isnumeric(): # 数字まで到達したら終了
                        break
                    else:
                        # before_sub_item_after_prefixには加算代入で連結
                        before_sub_item_after_prefix += s
                # split時にスペースが消えるため
                # スペースより前＋スペース＋後半の数字より前を
                # 現在扱っている項目の前方に挿入する
                sub_items[i] = before_sub_item_before+ ' ' + before_sub_item_after_prefix + sub_items[i]
        # 加工した内容をカンマ区切りの１つの文字列に戻す
        item = ",".join(sub_items)
        # 結果配列に追加
        result_items.append(item)
    else:
        # カンマが含まれていない場合結果配列に追加
        result_items.append(item)

print(result_items)
