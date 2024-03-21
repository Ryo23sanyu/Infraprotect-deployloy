mention = ["横桁 Cr0201,0301,0402 ⑦-d", "排管 Dp0201,0202 ①-c"]

result_items = []# 空のリストを作成
for item in mention:# mentionの要素の数だけitemに代入しループ
    parts = item.split(' ')  # スペースで分割して部品を取得
    key = parts[0]  # 先頭のキーワード（例: "横桁", "排管"）
    code_series = parts[1]  # コードシリーズ（例: "Cr0201,0301,0402"）
    suffix = parts[2]  # 末尾の注記（例: "⑦-d", "①-c"）

    codes = code_series.split(',')# code_seriesをコンマで分割
    new_code_series = []# 空のリストを作成
    for code in codes:# codesの要素の数だけcodeに代入しループ
        if not new_code_series:# new_code_seriesが空のとき
            new_code_series.append(code)# 最初のコードはそのまま追加
        else:# new_code_seriesが空でないとき
            prefix = ''.join(filter(str.isalpha, new_code_series[-1]))# 前のコードから記号を取得して新しいコードに追加
            # str.isalpha:文字列がアルファベット, new_code_series[-1]:new_code_seriesリストの最後の要素を取得
            # filter(str.isalpha, new_code_series[-1]):new_code_seriesリストの最後の要素からアルファベットのみを取得
            # '間に挿入する文字列'.join([連結したい文字列のリスト]):
            new_code = prefix + code
            new_code_series.append(new_code)

    # 新しいコードシリーズを結合して最終結果を作成
    new_item = f"{key} {','.join(new_code_series)} {suffix}"
    # key:（例: "横桁", "排管"）、{','.join(new_code_series)}:（例: "Cr0201,0301,0402"）、{suffix}:（例: "⑦-d", "①-c"）
    result_items.append(new_item)# result_itemsにnew_itemを格納

print(result_items)