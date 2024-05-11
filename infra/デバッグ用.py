import glob
import pprint
import re
from django.shortcuts import redirect, render
import ezdxf
from markupsafe import Markup

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
                    if not text.startswith("※"):
                        cad_data = text.split("\n") if len(text) > 0 else [] # .split():\nの箇所で配列に分配
                        # if len(cad_data) > 0 and not text.startswith("※") and not any(keyword in text for keyword in ["×", ".", "損傷図"]):
                        if len(cad_data) > 0 and not any(keyword in text for keyword in ["×", ".", "損傷図"]):
                    # 改行を含むかどうかをチェックする(and "\n" in cad):# 特定の文字列で始まるかどうかをチェックする: # 特定の文字を含むかどうかをチェックする
                            related_text = "" # 見つけたMTextと関連するDefpointsレイヤの文字列を代入する変数
                    # MTextの下、もしくは右に特定のプロパティ(Defpoints)で描かれた文字を探す
                            for neighbor in msp.query('MTEXT[layer=="Defpoints"]'): # DefpointsレイヤーのMTextを抽出
                            # MTextの挿入位置と特定のプロパティで描かれた文字の位置を比較する
                                if entity_extension(entity, neighbor):
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
                            
# << ※特記なき損傷の抽出用 >>                            
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
# << ※特記なき損傷の抽出用 >>
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
        
# extracted_text = [['主桁 Mg0101', '①-d', '写真番号-00', 'defpoints'], ['主桁 Mg0902', '⑦-c', '写真番号-00', 'defpoints']]
                
        # コンマが3つ以上存在する場合、3の倍数の位置で改行を挿入    
        def insert_line_breaks_on_commas(text):
            # コンマのカウントと改行の挿入を行う
            count = 0
            new_text = ''
            for char in text:
                if char == ',':
                    count += 1
                    if count % 3 == 0:
                        # 3, 6, 9番目のコンマの後に改行タグを挿入
                        new_text += ',</br>'
                        continue
                new_text += char
            return new_text
        
        # 正規表現を使って、コンマの直後に数字以外の文字が続く場所を見つけます。
        pattern = re.compile(r',(?![0-9])')
        # リスト内包表記で各要素をチェックして、条件に合致する場合は置き換えを行います。
        first_item = [Markup(insert_line_breaks_on_commas(pattern.sub(",</br>", sub_list[0]))) for sub_list in extracted_text]
        
    # リストの各要素から記号を削除する
        def remove_symbols(other_items):
            symbols = ['!', '[', ']', "'"]

            processed_other_items = []
            for item in other_items:
                processed_item = ''.join(c for c in item if c not in symbols)
                processed_other_items.append(processed_item)
    
            return processed_other_items
        
    # それ以外の要素(損傷名)を抽出
        pattern = r'[\u2460-\u2473\u3251-\u3256].*-[a-zA-Z]' # 丸数字とワイルドカードとアルファベット
        other_items = [[item for item in sub_list if isinstance(item, str) and re.match(pattern, item)] for sub_list in extracted_text]
        
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
               
        third_items = []
        bottom_item = []
        for sub_list in extracted_text:
            list_count = sum(isinstance(item, list) for item in sub_list) # リストの中にリストがいくつあるか数える
            
            if list_count == 2: # 座標が2つのとき=Defpointsが存在するとき
                bottom_item.append(sub_list[-3]) # 最後から3番目の要素を抽出（写真番号-00）
                third_items.append(sub_list[-4]) # 最後から4番目の要素を抽出（Defpoints）
            else:
                bottom_item.append("")
                third_items.append(None)

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
            if len(last_item)-1 < i:
                break

            if isinstance(last_item[i], list):
                continue
            else:
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

            item = {'first': first_item[i], 'second': second_items[i], 'third': third, 'last': picture_urls, 'picture': 'infra/noImage.png'}
            
            print("first_item:", first_item)
            print("second_items:", second_items)