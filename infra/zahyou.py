# <<テーブルの作成>>

def table_view(request):

    def extract_text(filename):
        doc = ezdxf.readfile(filename)
        msp = doc.modelspace()
        
        extracted_text = []
        for entity in msp:
            if entity.dxftype() == 'MTEXT':
                if entity.dxf.layer != 'Defpoints':
                # MTextのテキストを抽出する
                    text = entity.plain_text()
                    x, y, _ = entity.dxf.insert
                    coordinates = text + "\n" + str(x) + "\n" + str(y)
                    cad_data = coordinates.split("\n") if len(coordinates) > 0 else [] # .split():\nの箇所で配列に分配
                    if len(cad_data) > 0 and not coordinates.startswith("※") and not any(keyword in coordinates for keyword in ["×", ".", "損傷図"]):
                # 改行を含むかどうかをチェックする(and "\n" in cad):# 特定の文字列で始まるかどうかをチェックする: # 特定の文字を含むかどうかをチェックする
                        related_text = "" # 見つけたMTextと関連するDefpointsレイヤの文字列を代入する変数
                # MTextの下、もしくは右に特定のプロパティ(Defpoints)で描かれた文字を探す
                        for neighbor in msp.query('MTEXT[layer=="Defpoints"]'): # DefpointsレイヤーのMTextを抽出
                        # MTextの挿入位置と特定のプロパティで描かれた文字の位置を比較する
                            if entity_extension(entity, neighbor):
                            # 特定のプロパティ(Defpoints)で描かれた文字のテキストを抽出する
                                related_text = neighbor.plain_text()
                                defx, defy, _ = neighbor.dxf.insert
                                def_coordinates = text + "\n" + str(defx) + "\n" + str(defy)
                                def_data = def_coordinates.split("\n") if len(def_coordinates) > 0 else []
                            #extracted_text.append(neighbor_text)
                                break # 文字列が見つかったらbreakによりforループを終了する

                        if  len(related_text) > 0: #related_textに文字列がある＝Defpointsレイヤから見つかった場合
                            combined_list = cad_data + def_data # 見つかった文字列を追加する
                    #最後にまとめてcad_dataをextracted_textに追加する
                        extracted_text.append(combined_list)
        
        return extracted_text


    def entity_extension(mtext, neighbor):
        # MTextの挿入点
        mtext_insertion = mtext.dxf.insert
        # 特定のプロパティ(Defpoints)で描かれた文字の挿入点
        neighbor_insertion = neighbor.dxf.insert
        #テキストの行数を求める
        text = mtext.plain_text()
        text_lines = text.split("\n") if len(text) > 0 else []
        # 改行で区切ったリスト数→行数
        text_lines_count = len(text_lines)
        
        # Defpointsを範囲内とするX座標範囲
        x_start = mtext_insertion[0]  # X開始位置
        x_end  = mtext_insertion[0] + mtext.dxf.width # X終了位置= 開始位置＋幅
        y_start = mtext_insertion[1] + mtext.dxf.char_height # Y開始位置
        y_end  = mtext_insertion[1] - mtext.dxf.char_height * (text_lines_count + 1) # 文字の高さ×(行数+1)
        
        # MTextの下、もしくは右に特定のプロパティで描かれた文字が存在するかどうかを判定する(座標：右が大きく、上が大きい)
        if (
            neighbor_insertion[0] >= x_start and neighbor_insertion[0] <= x_end
        ):
            if ( #y_endの方が下部のため、y_end <= neighbor.y <= y_startとする
                neighbor_insertion[1] >= y_end and neighbor_insertion[1] <= y_start
            ):
                return True
        
        return False

    # AutoCADファイル名を指定してテキストを抽出する
    filename = R'C:\work\django\myproject\myvenv\Infraproject\uploads\121_損傷橋.dxf'
    extracted_text = extract_text(filename)

    for index, data in enumerate(extracted_text):
        # 最終項目-1まで評価
        if index < (len(extracted_text) -1):
            # 次の位置の要素を取得
            next_data = extracted_text[index + 1]
            # 特定の条件(以下例だと、１要素目が文字s1,s2,s3から始まる）に合致するかチェック
            if ("月" in next_data[0] and "日" in next_data[0]) or ("/" in next_data[0]) and (re.search(r"[A-Z]", next_data[0], re.IGNORECASE) and re.search(r"[0-9]", next_data[0])):
                # 合致する場合現在の位置に次の要素を併合 and "\n" in cad
                data.extend(next_data)
                # 次の位置の要素を削除
                extracted_text.remove(next_data)

    # 先頭の要素を抽出
        # 正規表現を使って、コンマの直後に数字以外の文字が続く場所を見つけます。
        pattern = re.compile(r',(?![0-9])')
        # リスト内包表記で各要素をチェックして、条件に合致する場合は置き換えを行います。
        first_item = [Markup(pattern.sub(",</br>", sub_list[0])) for sub_list in extracted_text]

    # リストの各要素から記号を削除する
        def remove_symbols(other_items):
            symbols = ['!', '[', ']', "'"]

            processed_other_items = []
            for item in other_items:
                processed_item = ''.join(c for c in item if c not in symbols)
                processed_other_items.append(processed_item)
    
            return processed_other_items
    # それ以外の要素を抽出
        other_items = [sub_list[1:-2] for sub_list in extracted_text]
        second = remove_symbols(other_items)
        
        # 丸数字を直接列挙
        circle_numbers = '①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳㉑㉒㉓㉔㉕㉖'
        
        second_items = []
        # リスト内の各文字列に対して処理を行う
        for second_over in second:
            # アルファベット(aからe)と直後に続く特定の丸数字の間にコンマを挿入
            if second_over == "":
                second_items.append(None)
            else:
                second_item = re.sub(f'([a-e])([{circle_numbers}])', r'\1,\2', second_over)
                second_split = second_item.split(",")
                second_items.append(second_split)
            
    # 最後から4番目の要素を抽出（写真番号-00）(写真番号-00,def,x座標,y座標)
        third_items = [sub_list[-4] for sub_list in extracted_text if len(sub_list) >= 3]
        
    # 最後から3番目の要素を抽出（Defpoints）(写真番号-00,def,x座標,y座標)
        bottom_item = [sub_list[-3] for sub_list in extracted_text]
        
        result_items = []# 配列を作成
        for item in bottom_item:# text_itemsの要素を1つずつitem変数に入れてforループする
            if ',' in item:# 要素の中にカンマが含まれている場合に実行
                sub_items = item.split(',')# カンマが含まれている場合カンマで分割
                extracted_item = []# 配列を作成
                for item in sub_items:# bottom_itemの要素を1つずつitem変数に入れてforループする
                    for p in range(len(item)):#itemの文字数をiに代入
                        if "A" <= item[p].upper() <= "Z" and p < len(item) - 1 and item[p+1].isnumeric():#i文字目がアルファベットかつ、次の文字が数字の場合
                            extracted_item.append(item[:p+1]+"*/*"+item[p+1:])# アルファベットと数字の間に*/*を入れてextracted_itemに代入
                            break
                join = ",".join(extracted_item)# 加工した内容をカンマ区切りの１つの文字列に戻す
                result_items.append(join)# result_itemsに格納

            else:# ifがfalseの場合(カンマが含まれていない場合)
                non_extracted_item = ''
                for j in range(len(item)):
                    if item[j].isalpha() and j < len(item) - 1 and item[j+1].isnumeric():#i文字目がアルファベットかつ、次の文字が数字の場合
                        non_extracted_item = item[:j+1]+"*/*"+item[j+1:]#アルファベットまでをextracted_itemに代入
                    elif non_extracted_item == '':
                        non_extracted_item = item
                result_items.append(non_extracted_item)

        def remove_parentheses_from_list(last):
            pattern = re.compile(r"\([^()]*\)")
            result = [pattern.sub("", string) for string in last]
            return result

        last_item = remove_parentheses_from_list(result_items)

        damage_table = []  # 空のリストを作成

    # ループで各要素を辞書型に変換し、空のリストに追加
        for i in range(len(first_item)):
            try:
                third = third_items[i]
            except IndexError:
                third = None
            
            # ['NON-a', '9月7日 S404', '9月7日 S537', '9月8日 S117,9月8日 S253']
            name_item = last_item[i].replace("S", "佐藤").replace("H", "濵田").replace(" ", "　")
            # name_item に格納されるのは 'NON-a', '9月7日 佐藤*/*404', '9月7日 佐藤*/*537', '9月8日 佐藤*/*117,9月8日 佐藤*/*253'のいずれかです。リストのi番目の文字列になります。

            dis_items = name_item.split(',') #「9月8日 S*/*117」,「9月8日 S*/*253」
            # コンマが付いていたら分割
            
            time_result = []
            current_date = ''  # 現在の日付を保持する変数
            for time_item in dis_items:
                # 先頭が数字で始まるかチェック（日付として扱えるか）
                if re.match(r'^\d', time_item):
                    current_date = re.match(r'^\d+月\d+日', time_item).group(0)  # 日付を更新
                    time_result.append(time_item)  # 日付がある項目はそのまま追加
                else:
                    # 日付がない項目は、現在の日付を先頭に追加
                    time_result.append(''.join([current_date, '　', time_item]))

            sub_dis_items = ['infra/static/infra/img/' + item + ".jpg" for item in time_result]
            # dis_itemsの要素の数だけ、分割した各文字の先頭に「infra/static/infra/img/」各文字の後ろに「.jpg」を追加
            # ['infra/static/infra/img/9月8日 S*/*117.jpg', 'infra/static/infra/img/9月8日 S*/*253.jpg']
            photo_paths = []
            # photo_pathsリストを作成
            for item in sub_dis_items:
                sub_photo_paths = glob.glob(item)
                photo_paths.extend(sub_photo_paths)
                # photo_pathsリストにsub_photo_pathsを追加
         
            if len(photo_paths) > 0:# photo_pathにはリストが入るため、[i]番目の要素が0より大きい場合
                picture_urls = [''.join(photo_path).replace('infra/static/', '') for photo_path in photo_paths]
                # photo_pathsの要素の数だけphoto_pathという変数に代入し、forループを実行
                # photo_pathという1つの要素の'infra/static/'を空白''に置換し、中間文字なしで結合する。
                # picture_urlsという新規配列に格納する。
            else:# それ以外の場合
                picture_urls = None
                #picture_urlsの値は[None]とする。

            item = {'first': first_item[i], 'second': second_items[i], 'third': third, 'last': picture_urls, 'picture': 'infra/img/noImage.png'}
            #items = [{'first': first_item[i], 'second': second_items[i], 'third': third, 'last': picture_urls, 'picture': 'infra/img/noImage.png'} for i in range(len(first_item))]    
            
            order_dict = {"主桁": 1, "横桁": 2, "床版": 3, "PC定着部": 4, "橋台[胸壁]": 5, "橋台[竪壁]": 6, "支承本体": 7, "沓座モルタル": 8, "防護柵": 9, "地覆": 10, "伸縮装置": 11, "舗装": 12, "排水ます": 13, "排水管": 14}
            #優先順位の指定
            order_number = {"None": 0, "①": 1, "②": 2, "③": 3, "④": 4, "⑤": 5, "⑥": 6, "⑦": 7, "⑧": 8, "⑨": 9, "⑩": 10, "⑪": 11, "⑫": 12, "⑬": 13, "⑭": 14, "⑮": 15, "⑯": 16, "⑰": 17, "⑱": 18, "⑲": 19, "⑳": 20, "㉑": 21, "㉒": 22, "㉓": 23, "㉔": 24, "㉕": 25, "㉖": 26}
            #優先順位の指定
            
            def sort_category(text): # sort_category関数を定義
                for key, val in order_dict.items(): # keyがキー(主桁～防護柵)、valが値(1～6)
                    if text.startswith(key): # textの1文字目がキー(主桁～防護柵)の場合
                        return val # 値(1～6)を返す
                return len(order_dict) # startswitchに全くマッチしなかった場合に実行(len(order_dict):6 → 順序はリストの末尾)
            
            def sort_number(second_text):
                num_text = second_text.split('-')[0]  # 例えば "①-d" の "①" の部分を取得
                for key, val in order_number.items():
                    if key == num_text:
                        return val
                return len(order_number)
            
            damage_table.append(item)
            sorted_text_list = sorted(damage_table, key=lambda text: (sort_category(text['first']), text['first'], sort_number('second')))
            # sorted(並び替えるオブジェクト, lamda式(無名関数)で並び替え 各要素: (text[0]で始まる要素を並び替え、その中でtext[0]の並び替え))

    context = {'damage_table': sorted_text_list}  # テンプレートに渡すデータ
    return render(request, 'table.html', context)