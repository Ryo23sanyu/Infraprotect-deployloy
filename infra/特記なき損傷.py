import re

extracted_text = "※特記なき損傷\n横桁 Cr0102 ①-d\n横桁 Cr0201,0301,0402 ⑦-d\n床版 Ds0101～0108 ⑪-c\n縦桁 Mg0101～0108,0201～0208 ①-d\n主桁 Mg0101～0208 ①-d\n横桁 Cr0101,0201,0301\n対傾構 Cf0102,0202,0302 ①-d\n防護柵 Gf0101,0401\n地覆 Fg0101,0401 ⑦-c,⑫-e\n縁石 Cu0201,0301\n㉓-c"
before = [['主桁 Mg0101', '①-d', '写真番号-00', 'defpoints'], ['主桁 Mg0902', '⑦-c', '写真番号-00', 'defpoints']]

if not extracted_text.startswith("※"):
    pass# なにもしない
else:
    lines = extracted_text.split('\n')# 改行でテキストを分割してリスト化
    sub_text = [[line] for line in lines]# 各行をサブリストとして持つ多重リストを構築

    pattern = r"\s[\u2460-\u3256]"# 文字列のどこかにスペース丸数字の並びがあるかをチェックする正規表現パターン
    pattern_start = r"^[\u2460-\u3256]"  # 文字列の開始が①～㉖であることをチェックする正規表現パターン
    pattern_anywhere = r"[\u2460-\u3256]"  # 文字列のどこかに①～㉖があるかをチェックする正規表現パターン
    last_found_circle_number = None  # 最後に見つかった丸数字を保持する変数

    # リストを逆順でループし、条件に応じて処理
    for i in range(len(sub_text)-1, -1, -1):  # 後ろから前にループ
        item = sub_text[i][0]  # textリストの各サブリストの最初の要素（[0]）をitem変数に代入（地覆 ㉓-c）
        if item.startswith("※"):
            sub_text.remove(sub_text[i]) # 配列から除外する
        elif re.search(pattern, item):  # itemが正規表現patternと一致している場合（スペース丸数字の並びがある）
            last_found = item  # last_found変数にitem要素を代入（地覆 ㉓-c）
            # print(last_found) 丸数字が付いている要素のみ出力
        elif 'last_found' in locals():  # last_foundが定義されている（要素が代入されている）場合のみ
            space = last_found.replace("　", " ")
            # 大文字スペースがあれば小文字に変換
            second = space.find(" ", space.find(" ") + 1)#10
            # 2つ目のスペース位置まで抽出
            sub_text[i][0] = item + last_found[second:]
            # item:スペース丸数字の並びがない文字列
            # last_found:スペース丸数字の並びがある文字列
            # last_found[second:]:スペースを含めた文字列
        elif re.match(pattern_start, item): # 文字列が①～㉖で開始するかチェック
            last_found_circle_number = item # 丸数字の入っている要素を保持
            sub_text.remove(sub_text[i])
        else:
            if last_found_circle_number is not None and not re.search(pattern_anywhere, item):
                # 要素に丸数字が含まれておらず、直前に丸数字が見つかっている場合
                sub_text[i][0] += " " + last_found_circle_number  # 要素の末尾に丸数字を追加

    # print(text)
    # [['横桁 Cr0102 ①-d'], ['横桁 Cr0201,0301,0402 ⑦-d'], ['床版 Ds0101～0108 ⑪-c']]
    # print(extracted_text)
    # [['主桁 Mg0101', '①-d', '写真番号-00', 'defpoints'], ['主桁 Mg0902', '⑦-c', '写真番号-00', 'defpoints']]

    for sub_list in sub_text:
        # サブリストの最初の要素を取得してスペース区切りで分割
        split_items = sub_list[0].split()
        
        # 分割した要素から必要なデータを取り出して新しいサブリストに格納
        header = split_items[0] + " " + split_items[1]  # 例：'主桁 Mg0101'
        status = split_items[2]  # 例：'①-d'
        # photo_number = '写真番号-00'
        # defpoints = 'defpoints'
        
        # 新しい形式のサブリストを作成してprocessed_listに追加
        # new_sub_list = [header, status, photo_number, defpoints]
        new_sub_list = [header, status]
        before.append(new_sub_list)

    # 処理後のリストを表示
    print(before)