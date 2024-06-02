import glob
import re
import ezdxf
from markupsafe import Markup

dxf_filename = R'C:\work\django\myproject\program\Infraproject\uploads\121_損傷橋.dxf'
search_title_text = "1径間" # 複数径間の場合は"1径間"
second_search_title_text = "損傷図"

def find_square_around_text(dxf_filename, target_text, second_target_text):
    doc = ezdxf.readfile(dxf_filename)
    msp = doc.modelspace()
    
    text_positions = [] # 見つかったテキストの位置を格納するためのリストを作成
    
    extracted_text = []

    # MTEXTエンティティの各要素をtextという変数に代入してループ処理
    for mtext_insert_point in msp.query('MTEXT'): # モデルスペース内の「MTEXT」エンティティをすべて照会し、ループ処理
        if mtext_insert_point.dxf.text == target_text: # エンティティのテキストが検索対象のテキストと一致した場合
            text_insertion_point = mtext_insert_point.dxf.insert # テキストの挿入点(dxf.insert)を取得します。
            text_positions.append(text_insertion_point[0]) # 挿入点のX座標をリストに保存
            break

    if not text_positions: # text_positionsリストが空の場合(見つけられなかった場合)
        for mtext_insert_point in msp.query('MTEXT'): # モデルスペース内の「MTEXT」エンティティをすべて照会し、ループ処理
            if mtext_insert_point.dxf.text == second_target_text: # エンティティのテキストが検索対象のテキストと一致した場合
                text_insertion_point = mtext_insert_point.dxf.insert # テキストの挿入点(dxf.insert)を取得します。
                text_positions.append(text_insertion_point[0]) # 挿入点のX座標をリストに保存
                break
    
    # Defpointsレイヤーで描かれた正方形枠の各要素をsquare変数に代入してループ処理
    for defpoints_square in msp.query('LWPOLYLINE[layer=="Defpoints"]'): # 
        if len(defpoints_square) == 4: # 正方形(=4辺)の場合
            square_x_values = [four_points[0] for four_points in defpoints_square] # squareというリストをループして各点(point)からx座標(インデックス0の要素)を抽出
            square_min_x = min(square_x_values) # 枠の最小X座標を取得
            square_max_x = max(square_x_values) # 枠の最大X座標を取得
            
        # 文字のX座標が枠の最小X座標と最大X座標の間にあるかチェック
        # text_positionsの各要素をtext_x_positionという変数に代入してforループを処理
        for text_x_position in text_positions:
            
            # 文字の座標がDefpoints枠のX座標内にある場合
            if square_min_x <= text_x_position <= square_max_x:
                
                # print(list(square)) 4点の座標を求める 
                left_top_point = list(defpoints_square)[0][0] # 左上の座標
                right_top_point = list(defpoints_square)[1][0] # 右上の座標
                right_bottom_point = list(defpoints_square)[2][0] # 右下の座標
                left_bottom_point = list(defpoints_square)[3][0] # 左下の座標

                defpoints_max_x = max(left_top_point,right_top_point,left_bottom_point,right_bottom_point) # X座標の最大値
                defpoints_min_x = min(left_top_point,right_top_point,left_bottom_point,right_bottom_point) # X座標の最小値
                
    # 指定したX座標範囲内にあるテキストを探す
    for circle_in_text in msp.query('MTEXT'):
        if defpoints_min_x <= circle_in_text.dxf.insert.x <= defpoints_max_x and circle_in_text.dxf.layer != 'Defpoints':
        # MTextのテキストを抽出する
            text = circle_in_text.plain_text()
            x, y, _ = circle_in_text.dxf.insert
            if not text.startswith("※"):
                cad_data = text.split("\n") if len(text) > 0 else [] # .split():\nの箇所で配列に分配
                # if len(cad_data) > 0 and not text.startswith("※") and not any(keyword in text for keyword in ["×", ".", "損傷図"]):
                if len(cad_data) > 0 and not any(keyword in text for keyword in ["×", ".", "損傷図"]) and not text.endswith("径間"):
            # 改行を含むかどうかをチェックする(and "\n" in cad):# 特定の文字列で始まるかどうかをチェックする: # 特定の文字を含むかどうかをチェックする
                    related_text = "" # 見つけたMTextと関連するDefpointsレイヤの文字列を代入する変数
            # MTextの下、もしくは右に特定のプロパティ(Defpoints)で描かれた文字を探す
                    for neighbor in msp.query('MTEXT[layer=="Defpoints"]'): # DefpointsレイヤーのMTextを抽出
                    # MTextの挿入位置と特定のプロパティで描かれた文字の位置を比較する
                        if entity_extension(circle_in_text, neighbor):
                        # 特定のプロパティ(Defpoints)で描かれた文字のテキストを抽出する
                            related_text = neighbor.plain_text()
                            defx, defy, _ = neighbor.dxf.insert
                        #extracted_text.append(neighbor_text)
                            break # 文字列が見つかったらbreakによりforループを終了する

                    if  len(related_text) > 0: #related_textに文字列がある＝Defpointsレイヤから見つかった場合
                        cad_data.append(related_text[:]) # cad_dataに「部材名～使用写真」までを追加
                        cad_data.append([str(x), str(y)]) # 続いてcad_dataに「MTEXT」のX,Y座標を追加
                #最後にまとめてcad_dataをextracted_textに追加する
                    extracted_text.append(cad_data[:] + [[str(defx), str(defy)]]) # extracted_textに「MTEXTとその座標」およびdefのX,Y座標を追加
                    
# << ※特記なき損傷の抽出用 ↓ >>                            
            else:
                lines = text.split('\n')# 改行でテキストを分割してリスト化
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
                    extracted_text.append(new_sub_list)

                    new_sub_list.append([str(x), str(y)])
# << ※特記なき損傷の抽出用 ↑ >>
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

extracted_text = find_square_around_text(dxf_filename, search_title_text, second_search_title_text) # 関数の定義

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
# extracted_text = [['主桁 Mg0101', '①-d', '写真番号-00', 'defpoints'], ['主桁 Mg0902', '⑦-c', '写真番号-00', 'defpoints']]

# それぞれのリストから文字列のみを抽出する関数(座標以外を抽出)
    def extract_text(data):
        extracted = []  # 空のリストを用意
        removed_elements = []  # バックアップ用リスト

        pattern = r'[\u2460-\u3256]'  # ⓵～㉖

        for list_item in data:  # list_item変数に要素を代入してループ処理
            # print(list_item)
            item_extracted = [item for item in list_item if isinstance(item, str)]
            
            if item_extracted:  # item_extractedが空でないことを確認
                # 最後の要素に特定の文字が含まれているかどうかをチェック
                contains_symbols = bool(re.search(pattern, item_extracted[-1]))

                # '月'と'日'が最後の要素に含まれているかどうかをチェック
                if '月' in item_extracted[-1] and '日' in item_extracted[-1] and not contains_symbols:
                    extracted.append(item_extracted[:-2])
                    # 座標や日時を削除し、removed_elementsに保存
                    removed_elements.append([item for item in list_item if item not in item_extracted[:-2]])
                else:
                    extracted.append(item_extracted)
                    # 座標や日時を削除し、removed_elementsに保存
                    removed_elements.append([item for item in list_item if item not in item_extracted])
            else:
                extracted.append([])
                removed_elements.append(list_item)

        return extracted, removed_elements  # extractedの結果を関数に返す

    # 関数を使って特定の部分を抽出
    extracted_text, removed_elements = extract_text(extracted_text)

    first_item = []
    current_detail = None  # 現在処理しているdetailを追跡

    for text, removed in zip(extracted_text, removed_elements):  # 1つずつのリスト
        result_list = []
        for item in text:# 1つずつの要素
        # 各条件を個別に確認する
            space_exists = re.search(r"\s+", item) is not None # スペースを含む
            alpha_exists = re.search(r"[a-zA-Z]+", item) is not None # アルファベットを含む
            digits_exists = re.search(r"\d{2,}", item) is not None # 2桁以上の数字を含む
        
            if space_exists and alpha_exists and digits_exists:
            # 新しいdetail項目を作成し、resultsに追加します
                current_detail = {'detail': item, 'items': []}
                result_list.append(current_detail)
            
            else:
            # 既存のdetailのitemsに現在の項目を追加
                if current_detail is not None:
                    current_detail['items'].append(item)
                
    # 元の要素を結果に追加
        for elem in removed:
            result_list.append(elem)

    #print(result_list)
        first_item.append(result_list)
    
    #print(first_item)
    extracted_text = first_item
        
    sub_first_item = [] 
    for check_sub_list in extracted_text:
        first_sub_item = []
        for first_sub_list in check_sub_list:
            # 各条件を個別に確認する
            space_exists = re.search(r"\s+", str(first_sub_list)) is not None # スペースを含む
            alpha_exists = re.search(r"[a-zA-Z]+", str(first_sub_list)) is not None # アルファベットを含む
            digits_exists = re.search(r"\d{2,}", str(first_sub_list)) is not None # 2桁以上の数字を含む
            # 正規表現を使って、コンマの直後に数字以外の文字が続く場所を見つけます。
            pattern = re.compile(r',(?![0-9])')
            # print(sub_list)
    # リスト内包表記で各要素をチェックして、条件に合致する場合は置き換えを行います。
            if space_exists and alpha_exists and digits_exists and not "月" in first_sub_list:
                # sub_list自体を文字列に変換するのではなく、detailフィールドのみを操作する
                detail_str = first_sub_list['detail']
                # detail_strのカンマの直後に`</br>`タグを挿入
                processed_str = pattern.sub(",", detail_str)
                # processed_strをMarkup関数を使ってHTML安全なマークアップに変換
                markup_str = Markup(processed_str)
                # markup_strをリストに包む
                wrapped_markup_str = [markup_str]
                # first_sub_itemリストに追加
                first_sub_item.append(wrapped_markup_str)
        sub_first_item.append(first_sub_item)
    # [[[Markup('横桁 Cr0503')]], [[Markup('主桁 Mg0110')], [Markup('床版 Ds0101')]], [[Markup('横桁 Cr0802')]], [[Markup('排水ます Dr0102,0201')]], [[Markup('排水ます Dr0202')]], [[Markup('PC定着部 Cn1101')]], [[Markup('排水ます Dr0102,0201,0202')]]]

        def process_item(item):
            if isinstance(item, Markup):
                item = str(item)
            
            if ',' in item:
                sub_items = item.split(',')
                for i, sitem in enumerate(sub_items):
                    if i > 0 and sitem[0].isnumeric():
                        before_sub_item = sub_items[i - 1]
                        before_sub_item_splitted = before_sub_item.split()
                        before_sub_item_prefix = before_sub_item_splitted[0]
                        before_sub_item_suffix = ''
                        
                        for char in before_sub_item_splitted[1]:
                            if char.isnumeric():
                                break
                            else:
                                before_sub_item_suffix += char
                        
                        sub_items[i] = before_sub_item_prefix + ' ' + before_sub_item_suffix + sitem
                item = ",".join(sub_items)
            
            return item.split(',')

        first_item = []
        for sub_one in sub_first_item:
            append2 = []
            for text_items in sub_one:
                result_items = []
                for item in text_items:
                    processed_items = process_item(item)
                    result_items.extend(processed_items)
                append2.append(result_items)
            first_item.append(append2)

    # << ◆損傷種類(second)の要素◆ >> 
    # リストの各要素から記号を削除する関数
    def remove_symbols(other_items):
        symbols = ['!', '[', ']', "'"]

        processed_other_items = []
        for item in other_items:
            processed_item = ''.join(c for c in item if c not in symbols)
            processed_other_items.append(processed_item)

        return processed_other_items
    
    # それ以外の要素(損傷名)を抽出
    pattern = r'[\u2460-\u2473\u3251-\u3256].*-[a-zA-Z]' # 丸数字とワイルドカードとアルファベット
    second_items = []
    for second_sub_list in extracted_text:
        filtered_sub_list = []
        for damage_item in second_sub_list:
            if 'items' in damage_item:
            # sub_list自体を文字列に変換するのではなく、detailフィールドのみを操作する
                detail_damage = damage_item['items']
                for split_detail_damage in detail_damage:
                    if "," in split_detail_damage:
                        join_detail_damage = ""
                        middle_damage = split_detail_damage.split(",")
                        join_detail_damage = middle_damage
                    else:
                        join_detail_damage = detail_damage
                        
                filtered_sub_list.append(join_detail_damage)
        second_items.append(filtered_sub_list)

    third_items = []
    bottom_item = []
    damage_coordinate = []
    picture_coordinate = []
    for other_sub_list in extracted_text:
        list_count = sum(isinstance(item, list) for item in other_sub_list) # リストの中にリストがいくつあるか数える
        
        if list_count == 2: # 座標が2つのとき=Defpointsが存在するとき
            bottom_item.append(other_sub_list[-3]) # 最後から3番目の要素を抽出（写真番号-00）
            third_items.append(other_sub_list[-4]) # 最後から4番目の要素を抽出（Defpoints）
            damage_coordinate.append(other_sub_list[-2])
            picture_coordinate.append(other_sub_list[-1])
        else: # Defpointsがない時
            bottom_item.append("") # bottom:写真番号なし
            third_items.append(None) # third:Defpointsなし
            damage_coordinate.append(other_sub_list[-1]) # damage:
            picture_coordinate.append(None) # picture:写真指定なし
    #print(other_sub_list)
    
    result_items = []# 配列を作成
    for item in bottom_item:# text_itemsの要素を1つずつitem変数に入れてforループする
        if ',' in item:# 要素の中にカンマが含まれている場合に実行
            pattern = r',(?![^(]*\))'
            sub_items = re.split(pattern, item)# カンマが含まれている場合カンマで分割
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
                if "A" <= item[j].upper() <= "Z" and j < len(item) - 1 and item[j+1].isnumeric():#i文字目がアルファベットかつ、次の文字が数字の場合
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

    # first_itemの要素の数だけループ処理
    for i in range(len(first_item)):
        try:
            third = third_items[i]
        except IndexError:
            third = None
        
        # ['NON-a', '9月7日 S404', '9月7日 S537', '9月8日 S117,9月8日 S253']
        if len(last_item)-1 < i:
            break

        if isinstance(last_item[i], list):
            continue
        else:
            name_item = last_item[i].replace("S", "佐藤").replace("H", "濵田").replace(" ", "　")
        # name_item に格納されるのは 'NON-a', '9月7日 佐藤*/*404', '9月7日 佐藤*/*537', '9月8日 佐藤*/*117,9月8日 佐藤*/*253'のいずれかです。リストのi番目の文字列になります。

        pattern = r',(?![^(]*\))'
        dis_items = re.split(pattern, name_item)#「9月8日 S*/*117」,「9月8日 S*/*253」
        # コンマが付いていたら分割
        
        time_result = []
        current_date = ''  # 現在の日付を保持する変数
        for time_item in dis_items:
            #print(f"このデータは：{time_item}")
            # 先頭が数字で始まるかチェック（日付として扱えるか）
            if re.match(r'^\d', time_item):
                current_date = re.match(r'^\d+月\d+日', time_item).group(0)  # 日付を更新
                time_result.append(time_item)  # 日付がある項目はそのまま追加
            else:
                # 日付がない項目は、現在の日付を先頭に追加
                time_result.append(''.join([current_date, '　', time_item]))

        sub_dis_items = ['infra/static/infra/img/' + item + ".jpg" for item in time_result]
        #print(sub_dis_items)
        # dis_itemsの要素の数だけ、分割した各文字の先頭に「infra/static/infra/img/」各文字の後ろに「.jpg」を追加
        # ['infra/static/infra/img/9月8日 S*/*117.jpg', 'infra/static/infra/img/9月8日 S*/*253.jpg']
        # print(f"このデータは：{sub_dis_items}")
        photo_paths = []
        # photo_pathsリストを作成
        for item in sub_dis_items:
            sub_photo_paths = glob.glob(item)
            photo_paths.extend(sub_photo_paths)
            # photo_pathsリストにsub_photo_pathsを追加
        # print(photo_paths)
        if len(photo_paths) > 0:# photo_pathにはリストが入るため、[i]番目の要素が0より大きい場合
            picture_urls = [''.join(photo_path).replace('infra/static/', '') for photo_path in photo_paths]
            
            # photo_pathsの要素の数だけphoto_pathという変数に代入し、forループを実行
            # photo_pathという1つの要素の'infra/static/'を空白''に置換し、中間文字なしで結合する。
            # picture_urlsという新規配列に格納する。
        else:# それ以外の場合
            picture_urls = None
            #picture_urlsの値は[None]とする。

# << ◆写真メモを作成するコード◆ >>

        bridge_damage = [] # すべての"bridge"辞書を格納するリスト

        bridge = {
            "first": first_item[i],
            "second": second_items[i] if i < len(second_items) else None  # second_itemsが足りない場合にNoneを使用
        }
        bridge_damage.append(bridge)
        #print(bridge_damage)
        
# << ◆1つ1つの部材に対して損傷を紐付けるコード◆ >>
        first_element = bridge_damage[0]

        # 'first'キーの値にアクセス
        first_value = first_element['first']

        first_and_second = []
        #<<◆ 部材名が1種類かつ部材名の要素が1種類の場合 ◆>>
        if len(first_value) == 1: # 部材名称が1つの場合
            if len(first_value[0]) == 1: # 要素が1つの場合
                # カッコを1つ減らすためにリストをフラットにする
                flattened_first = [first_buzai_item for first_buzai_sublist in first_value for first_buzai_item in first_buzai_sublist]
                first_element['first'] = flattened_first
                # 同様に 'second' の値もフラットにする
                second_value = first_element['second']
                flattened_second = [second_name_item for second_name_sublist in second_value for second_name_item in second_name_sublist]
                first_element['second'] = flattened_second
                
                first_and_second.append(first_element)
                #print(first_and_second) # [{'first': ['排水管 Dp0102'], 'second': ['①腐食(小大)-c', '⑤防食機能の劣化(分類1)-e']}]
                
            #<<◆ 部材名が1種類かつ部材名の要素が複数の場合 ◆>>
            else: # 別の部材に同じ損傷が紐付く場合
                    # 元のリストから各要素を取得
                for first_buzai_item in bridge_damage:
                    #print(item)
                    first_elements = first_buzai_item['first'][0]  # ['床版 Ds0201', '床版 Ds0203']
                    second_elements = first_buzai_item['second'][0]  # ['⑦剥離・鉄筋露出-d']
                    
                    # first の要素と second を一対一で紐付け
                    for first_buzai_second_name in first_elements:
                        if "～" in first_buzai_second_name:

                            first_step = first_buzai_second_name

                            if " " in first_step:
                                # 部材記号の前にスペースが「含まれている」場合
                                first_step_split = first_step.split()

                            else:
                                # 部材記号の前にスペースが「含まれていない」場合
                                first_step_split = re.split(r'(?<=[^a-zA-Z])(?=[a-zA-Z])', first_step) # アルファベット以外とアルファベットの並びで分割
                                first_step_split = [kara for kara in first_step_split if kara] # re.split()の結果には空文字が含まれるので、それを取り除く

                            # 正規表現
                            number = first_step_split[1]
                            # マッチオブジェクトを取得

                            # マッチオブジェクトを取得
                            number_part = re.search(r'[A-Za-z]*(\d+～\d+)', number).group(1)

                            one = number_part.find("～")

                            start_number = number_part[:one]
                            end_number = number_part[one+1:]

                            # 最初の2桁と最後の2桁を取得
                            start_prefix = start_number[:2]
                            start_suffix = start_number[2:]
                            end_prefix = end_number[:2]
                            end_suffix = end_number[2:]

                            # 「主桁 Mg」を抽出
                            prefix_text = first_step_split[0] + " " + re.match(r'[A-Za-z]+', number).group(0)

                            number_arrangement = []
                            for prefix in range(int(start_prefix), int(end_prefix)+1):
                                for suffix in range(int(start_suffix), int(end_suffix)+1):
                                    number_items = "{}{:02d}{:02d}".format(prefix_text, prefix, suffix)
                                    sub_first_and_second = {'first': [number_items], 'second': second_elements}
                                    first_and_second = [sub_first_and_second]
                        else:
                            sub_first_and_second = {'first': [first_buzai_second_name], 'second': second_elements}
                            first_and_second = [sub_first_and_second]
            #print(first_and_second) # [{'first': '床版 Ds0201', 'second': '⑦剥離・鉄筋露出-d'}, {'first': '床版 Ds0203', 'second': '⑦剥離・鉄筋露出-d'}]

        #<<◆ 部材名が複数の場合 ◆>>
        else:
            for double_item in bridge_damage:
                first_double_elements = double_item['first'] # [['支承本体 Bh0101'], ['沓座モルタル Bm0101']]
                second_double_elements = double_item['second'] # [['①腐食(小小)-b', '⑤防食機能の劣化(分類1)-e'], ['⑦剥離・鉄筋露出-c']]
                
                for break_first, break_second in zip(first_double_elements, second_double_elements):
                    first_and_second.append({'first': break_first, 'second': break_second})

        for damage_parts in bridge_damage:
            # print(damage_parts)
            if isinstance(damage_parts["second"], list):  # "second"がリストの場合
                filtered_second_items = []
                for sublist in damage_parts["second"]:
                    if isinstance(sublist, list):  # サブリストがリストである場合
                        if any(item.startswith('①') for item in sublist) and any(item.startswith('⑤') for item in sublist):
                            # ⑤で始まる要素を取り除く
                            filtered_sublist = [item for item in sublist if not item.startswith('⑤')]
                            filtered_second_items.append(filtered_sublist)
                        else:
                            filtered_second_items.append(sublist)
                    else:
                        filtered_second_items.append([sublist])
                
                # フィルタリング後のsecond_itemsに対して置換を行う                
                #pavement_items = {"first": first_item[i], "second": filtered_second_items}
                    
        combined_list = []
        if damage_parts["second"] is not None:
            combined_second = filtered_second_items #if i < len(updated_second_items) else None
        else:
            combined_second = None
        
        combined = {"first": first_item[i], "second": combined_second}
        combined_list.append(combined)
        request_list = combined_list[0]
        # <<◆ secondの多重リストを統一させる ◆>>
        try:
            # データを取得する
            check_request_list = request_list['first'][1]

            # 条件分岐
            if isinstance(check_request_list, list):
                request_list
                #print(request_list)
                
        except (KeyError, IndexError) as e:
            # KeyError や IndexError の例外が発生した場合の処理

            # secondの多重リストをフラットなリストに変換
            flat_list = [item for sublist in request_list['second'] for item in sublist]
            # フラットなリストを再びサブリストに変換して格納
            request_list['second'] = [flat_list]
            # 完成目標の確認
            
            test = request_list['second'][0]

        # 先頭が文字（日本語やアルファベットなど）の場合
        def all_match_condition(lst):
            """
            リスト内のすべての項目が特定条件に一致するか確認します。
            ただし、空のリストの場合、Falseを返します。
            """
            # 空のリストの場合は False を返す
            if not lst:
                return False
            
            pattern = re.compile(r'\A[^\W\d_]', re.UNICODE)
            return all(pattern.match(item) for item in lst)

        if all_match_condition(test):
            request_list
        else:
            request_list['second'] = [request_list['second']]

        #<< ◆損傷メモの作成◆ >>
        replacement_patterns = {
            "①腐食(小小)-b": "腐食", # 1
            "①腐食(小大)-c": "拡がりのある腐食",
            "①腐食(大小)-d": "板厚減少を伴う腐食",
            "①腐食(大大)-e": "板厚減少を伴う拡がりのある腐食",
            "③ゆるみ・脱落-c": "ボルト、ナットにゆるみ・脱落（●本中●本）",
            "③ゆるみ・脱落-e": "ボルト、ナットにゆるみ・脱落（●本中●本）", # 3
            "④破断-e": "鋼材の破断", # 4
            "⑤防食機能の劣化(分類1)-e": "点錆", # 5
            "⑥ひびわれ(小小)-b": "最大幅0.0mmのひびわれ", # 6
            "⑥ひびわれ(小大)-c": "最大幅0.0mmかつ間隔0.5m未満のひびわれ",
            "⑥ひびわれ(中小)-c": "最大幅0.0mmのひびわれ",
            "⑥ひびわれ(中大)-d": "最大幅0.0mmかつ間隔0.5m未満のひびわれ",
            "⑥ひびわれ(大小)-d": "最大幅0.0mmのひびわれ",
            "⑥ひびわれ(大大)-e": "最大幅0.0mmかつ間隔0.5m未満のひびわれ",
            "⑦剥離・鉄筋露出-c": "コンクリートの剥離", # 7
            "⑦剥離・鉄筋露出-d": "鉄筋露出",
            "⑦剥離・鉄筋露出-e": "断面減少を伴う鉄筋露出",
            "⑧漏水・遊離石灰-c": "漏水", # 8
            "⑧漏水・遊離石灰-d": "遊離石灰",
            "⑧漏水・遊離石灰-e": "著しい遊離石灰・泥や錆汁の混入を伴う漏水",
            "⑨抜け落ち-e": "コンクリート塊の抜け落ち", # 9
            "⑪床版ひびわれ-b": "最大幅0.0mmの1方向ひびわれ",
            "⑪床版ひびわれ-c": "最大幅0.0mmの1方向ひびわれ",
            "⑪床版ひびわれ-d": "最大幅0.0mmの1方向ひびわれ",
            "⑪床版ひびわれ-e": "最大幅0.0mmの角落ちを伴う1方向ひびわれ", # 11
            "⑫うき-e": "コンクリートのうき", # 12
            "⑮舗装の異常-c": "最大幅0.0mmのひびわれ",
            "⑮舗装の異常-e": "最大幅0.0mmのひびわれ・舗装の土砂化", # 15
            "⑯定着部の異常-c": "定着部の損傷。",
            "⑯定着部の異常(分類2)-e": "定着部の著しい損傷", # 16
            "⑳漏水・滞水-e": "漏水・滞水", # 20
            "㉓変形・欠損-c": "変形・欠損", # 23
            "㉓変形・欠損-e": "著しい変形・欠損",
            "㉔土砂詰まり-e": "土砂詰まり", # 24
        }

        def describe_damage(unified_request_list):
            described_list = []
            
            for damage in unified_request_list:
                if damage in replacement_patterns:
                    described_list.append(replacement_patterns[damage])
                elif damage.startswith('⑰'):
                    match = re.search(r'(?<=:)(.*?)(?=\)-e)', damage)
                    if match:
                        described_list.append(match.group(1))
                else:
                    pattern = r'[\u3248-\u3257](.*?)-'
                    match = re.search(pattern, damage)
                    if match:
                        described_list.append(match.group(1))
                    else:
                        described_list.append(damage)  # フォールバックとしてそのまま返す
            return ','.join(described_list)

        # 各ケースに対して出力を確認:
        def generate_report(unified_request_list):
            primary_damages = []
            processed_related_damages = []
            #print(f"unified_request_list：{unified_request_list}")
            first_items = unified_request_list['first']
            #print(first_items) # [['支承本体 Bh0101'], ['沓座モルタル Bm0101']]
            second_items = unified_request_list['second']
            #print(second_items) # [['①腐食(小小)-b', '⑤防食機能の劣化(分類1)-e'], ['⑦剥離・鉄筋露出-c']]
            primary_damages_dict = {}

            for first_item, second_item in zip(first_items, second_items):
                #print(f"first_items：{first_items}")
                #print(f"second_items：{second_items}")
                #print(f"first_item：{first_item}")
                #print(f"second_item：{second_item}")
                element_names = [f.split()[0] for f in first_item] # カッコ内の要素について、スペースより前を抽出
                #print(f"element_names：{element_names}") # ['支承本体'], ['沓座モルタル']
                damage_descriptions = describe_damage(second_item) # 辞書で置換
                #print(f"damage_descriptions：{damage_descriptions}") # 腐食,点錆, 剥離
                
                if len(element_names) == 1: # ['主桁', '横桁', '対傾構']：これはだめ
                    primary_damages.append(f"{element_names[0]}に{damage_descriptions}が見られる。")
                    #print(f"primary_damages：{primary_damages}") # ['支承本体に腐食,点錆が見られる。', '沓座モルタルに剥離が見られる。']
                else:
                    element_names = list(dict.fromkeys(element_names))            
                    joined_elements = "および".join(element_names[:-1]) + "," + element_names[-1]
                    if joined_elements.startswith(","):
                        new_joined_elements = joined_elements[1:]
                    else:
                        new_joined_elements = joined_elements
                    primary_damages.append(f"{new_joined_elements}に{damage_descriptions}が見られる。")

                for elem in first_item:
                    primary_damages_dict[elem] = second_item[:]

            primary_description = "また".join(primary_damages)
                
            for elem_name, elem_number in zip(first_items, second_items): # 主桁 Mg0101
                #print(f"{first_items}-{elem_name}")
                #print(f"{second_items}-{elem_number}")
                #print(len(first_items))
                #print(len(second_items))
                #print(" ")
                # リストをフラットにする関数
                def flatten_list(nested_list):
                    return [item for sublist in nested_list for item in sublist]
                
                # 辞書から 'first' と 'second' の値を取り出す
                first_list = request_list['first']
                second_list = request_list['second']

                # 'first' の要素数を数える
                first_count = sum(len(sublist) for sublist in first_list)

                # 'second' の要素数を数える
                second_count = sum(len(sublist) for sublist in second_list)
                # フラットにしたリストを比較
                if flatten_list(first_items) != elem_name and flatten_list(second_items) != elem_number:
                    #print(f"{flatten_list(first_items)}-{elem_name}")
                    #print(f"{flatten_list(second_items)}-{elem_number}")
                    sub_related_damages = []
                    for first_item in first_items:
                        for elem in first_item:
                            if elem in primary_damages_dict:
                                formatted_damages = ",".join(list(dict.fromkeys(primary_damages_dict[elem])))
                                sub_related_damages.append(f"{elem}:{formatted_damages}")
                                #print(f"sub_related_damages：{sub_related_damages}") # ['支承本体 Bh0101:①腐食(小小)-b,⑤防食機能の劣化(分類1)-e', '沓座モルタル Bm0101:⑦剥離・鉄筋露出-c']

                    # 処理後のリストを格納するための新しいリスト
                    second_related_damages = []

                    # リスト内の各要素をループする
                    for i, damage in enumerate(sub_related_damages):
                        # コロンの位置を取得
                        colon_index = damage.find(":")
                        
                        if colon_index != -1:
                            if i == 0:
                                # 1番目の要素の場合
                                parts = damage.split(',')
                                
                                if len(parts) > 1:
                                    first_damage = parts[0].split(':')[0]
                                    after_damage = ':' + parts[1].strip()
                                    create_damage = first_damage + after_damage
                                    second_related_damages.append(create_damage)

                            else:
                                # 2つ目以降の要素の場合
                                parts = damage.split(',')
                                second_related_damages.append(damage)
                                

                    # 処理後のリストを格納するための新しいリスト
                    processed_related_damages = []
                    #print(f"second_related_damages：{second_related_damages}")
                    for damage in second_related_damages:
                        colon_index = damage.find(":")
                        if colon_index != -1:
                            before_colon_part = damage[:colon_index].strip()
                            after_colon_part = damage[colon_index + 1:].strip()
                            #print(f"damage[colon_index + 1:]：{damage}")
                            if before_colon_part and after_colon_part:
                                processed_damage = f"{before_colon_part}:{after_colon_part}"
                                processed_related_damages.append(processed_damage)
                    #print(f"after_colon_part：{processed_related_damages}")
                    
                elif first_count < 2 and second_count < 2: # {'first': [['横桁 Cr0803']], 'second': [['⑦剥離・鉄筋露出-d']]}
                    None
                elif first_count > 1 and second_count < 2: # {'first': [['床版 Ds0201', '床版 Ds0203']], 'second': [['⑦剥離・鉄筋露出-d']]}
                    #print(f"first_item：{first_item}") # ['床版 Ds0201', '床版 Ds0203']
                    #print(f"second_item：{second_item}") # ['⑦剥離・鉄筋露出-d']
                    first_items_from_first = first_item[1:]
                    #print(first_items_from_first) # ['橋台[竪壁] Ac0101', '伸縮装置 Ej0101']
                    related_damage_list = ','.join(first_items_from_first)# カンマ区切りの文字列に結合
                    #print(related_damage_list) # 橋台[竪壁] Ac0101,伸縮装置 Ej0101
                    related_second_item = ','.join(second_item)
                    processed_related_damages.append(f"{related_damage_list}:{related_second_item}")
                    #print(f"2-1_processed_related_damages：{processed_related_damages}")
                elif first_count < 2 and second_count > 1: # {'first': [['横桁 Cr0503']], 'second': [['⑦剥離・鉄筋露出-d', '⑰その他(分類6:施工不良)-e']]}
                    #print(first_item) # ['横桁 Cr0503']
                    #print(second_item) # ['⑦剥離・鉄筋露出-d', '⑰その他(分類6:施工不良)-e']
                    second_items_from_second = second_item[1:]
                    related_damage_list = ','.join(second_items_from_second)# カンマ区切りの文字列に結合
                    #print(related_damage_list)
                    processed_related_damages.append(f"{','.join(elem_name)}:{related_damage_list}")
                    #print(f"1-2_processed_related_damages：{processed_related_damages}")
                else:#  len(elem_name) > 1 and len(elem_number) > 1: # {'first': [['排水管 Dp0101', '排水管 Dp0102']], 'second': [['①腐食(小大)-c', '⑤防食機能の劣化(分類1)-e']]}
                    #print(first_item) # ['排水管 Dp0101', '排水管 Dp0102']
                    #print(second_item) # ['①腐食(小大)-c', '⑤防食機能の劣化(分類1)-e']
                    related_damage_list = ','.join(second_item)
                    #print(related_damage_list)
                    processed_related_damages.append(f"{','.join(elem_name)}:{related_damage_list}")
                    #print(f"0-0_processed_related_damages：{processed_related_damages}")


            related_description = ""
            if processed_related_damages:
                related_description = "\n【関連損傷】\n" + ", ".join(processed_related_damages)

            return f"{primary_description} {related_description}".strip()

        combined_data = generate_report(request_list)
        #print(combined_data)

        # << ◆ ここまで ◆ >>                   
                # \n文字列のときの改行文字
        items = {'first': first_item[i], 'second': second_items[i], 'join': first_and_second, 'third': third, 'last': picture_urls, 'picture': 'infra/noImage.png', 'textarea_content': combined_data, 'damage_coordinate': damage_coordinate[i], 'picture_coordinate': picture_coordinate[i]}
        
        damage_table.append(items)
    print(damage_table)