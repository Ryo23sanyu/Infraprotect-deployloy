import glob
import re

from markupsafe import Markup

text = [['横桁 Cr0503', '⑦剥離・鉄筋露出-d', '⑰その他(分類6:施工不良)-e', '写真番号-10,11', '9月7日 S450,S452(前-6,7)', ['546181.340571892', '222553.0807470059'], ['546769.9402349197', '222164.8389810835']], \
  ['主桁 Mg0110', '⑧漏水・遊離石灰-e', '床版 Ds0101', '⑦剥離・鉄筋露出-d', '⑪床版ひびわれ-d', '写真番号-16', '9月7日 S497(前-11)', ['531595.7611265536', '227530.3566962298'], ['531805.9667048807', '227218.1705246582']], \
    ['横桁 Cr0802', '⑥ひびわれ(大小)-d', '写真番号-10,11', '9月7日 S412(前-1)', ['538336.707491893', '217676.1803115158'], ['538925.3071549207', '217287.9385455934']], \
      ['排水ます Dr0102,0201', '①腐食(大小)-d', '⑤防食機能の劣化(分類1)-e', '写真番号-15,16', '9月7日 S503', ['524707.6595413402', '222788.7170443565'], ['525296.2592043679', '222400.4752784341']], \
        ['排水ます Dr0202', '①腐食(大小)-d', '⑤防食機能の劣化(分類1)-e', '写真番号-20', '9月7日 S511', ['524707.6595413402', '217928.9179385742'], ['525296.2592043679', '217540.6761726518']], \
          ['PC定着部 Cn1101', '⑯定着部の異常(分類2)-e', ['525296.2592043679', '217540.6761726518']], \
            ['排水ます Dr0102,0201,0202', '⑰その他(分類6:埋没)-e', ['521480.6484975223', '214010.8503334253']]]

# それぞれのリストから文字列のみを抽出する関数(座標以外を抽出)
def extract_text(data):
    extracted = []  # 空のリストを用意
    removed_elements = []  # バックアップ用リスト
    for list_item in data:  # list_item変数に要素を代入してループ処理
        item_extracted = [item for item in list_item if isinstance(item, str)]
        # item_extractedリストの最後の要素で条件をチェック
        pattern = r'[\u2460-\u3256]'# ⓵～㉖
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

    return extracted, removed_elements  # extractedの結果を関数に返す

# 関数を使って特定の部分を抽出
extracted_text, removed_elements = extract_text(text)

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

#<< テスト >>
# コンマが3つ以上存在する場合、3の倍数の位置で改行を挿入する関数
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
      
first_item = [] 
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
            modified_str = pattern.sub(",</br>", detail_str)
            # さらにinsert_line_breaks_on_commas関数を利用して処理
            processed_str = insert_line_breaks_on_commas(modified_str)
            # processed_strをMarkup関数を使ってHTML安全なマークアップに変換
            markup_str = Markup(processed_str)
            # markup_strをリストに包む
            wrapped_markup_str = [markup_str]
            # first_sub_itemリストに追加
            first_sub_item.append(wrapped_markup_str)
    first_item.append(first_sub_item)     
#print(first_item)
# [[[Markup('横桁 Cr0503')]], [[Markup('主桁 Mg0110')], [Markup('床版 Ds0101')]], [[Markup('横桁 Cr0802')]], [[Markup('排水ます Dr0102,0201')]], [[Markup('排水ます Dr0202')]], [[Markup('PC定着部 Cn1101')]], [[Markup('排水ます Dr0102,0201,0202')]]]

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
            # first_sub_itemリストに追加
            filtered_sub_list.append(detail_damage)
    second_items.append(filtered_sub_list)
#print(second_items)

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

last_item = bottom_item

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

    pattern = r', (?![^()]*\))'
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
    # dis_itemsの要素の数だけ、分割した各文字の先頭に「infra/static/infra/img/」各文字の後ろに「.jpg」を追加
    # ['infra/static/infra/img/9月8日 S*/*117.jpg', 'infra/static/infra/img/9月8日 S*/*253.jpg']
    # print(f"このデータは：{sub_dis_items}")
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
        

    bridge_damage = [] # すべての"bridge"辞書を格納するリスト

    bridge = {
    "first": first_item[i],
    "second": second_items[i] if i < len(second_items) else None  # second_itemsが足りない場合にNoneを使用
    }
    bridge_damage.append(bridge)

    replacement_patterns = {
    "①腐食(小小)-b": "腐食", # 1
    "①腐食(小大)-c": "拡がりのある腐食",
    "①腐食(大小)-d": "板厚減少を伴う腐食",
    "①腐食(大大)-e": "板厚減少を伴う拡がりのある腐食",
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
    "⑫うき-e": "コンクリートのうき", # 12
    "⑮舗装の異常-c": "最大幅0.0mmのひびわれ", # 15
    "⑮舗装の異常-e": "最大幅0.0mmのひびわれ・舗装の土砂化",
    "⑳漏水・滞水-e": "漏水・滞水", # 20
    "㉓変形・欠損-c": "変形・欠損", # 23
    "㉓変形・欠損-e": "著しい変形・欠損",
    "㉔土砂詰まり-e": "土砂詰まり", # 24
    }

    pavement_items = []
    for damage_parts in bridge_damage:
        for damage_name_text in damage_parts:
           pavement_items.append(str(damage_name_text))

    updated_second_items = []  # 更新されたsecond_itemsを格納するための新しいリスト

    for damage_number_items in second_items:#◆
        if damage_number_items is None:#◆
            updated_second_items.append(damage_number_items)#◆
            continue

        # '①'で始まる要素があるか確認
        has_item_starting_with_1 = any(item.startswith('①') for item in damage_number_items)#◆

        # '①'で始まる要素がある場合、'⑤'で始まる要素を削除
        if has_item_starting_with_1:
            updated_items = [damage_five_item for damage_five_item in damage_number_items if not damage_five_item.startswith('⑤')]#◆#★★★
        else:
            updated_items = damage_number_items.copy()  # items自体を直接変更しないためのコピー#◆

        # '⑰'で始まる要素があるか確認
        if any(seventeen_item.startswith('⑰') for seventeen_item in updated_items):#★★
            new_sublist = []
            # '⑰'で始まる要素がある場合、'⑰'のカッコ内の値のみ抽出
            for inside_name_item in updated_items:#★
                if inside_name_item.startswith('⑰'):#★
                    match = re.search(r'(?<=:)(.*?)(?=\)-e)', inside_name_item)#★
                    if match:
                        new_sublist.append(match.group(1))
                    else:
                        new_sublist.append(inside_name_item)  # マッチしなかった場合は元のアイテムを保持#★
                else:
                    new_sublist.append(inside_name_item)  # '⑰'で始まらないアイテムはそのまま追加#★
            updated_items = new_sublist  # 更新されたサブリストを反映

        updated_second_items.append(updated_items)
            

    # 処理結果を確認
    # first_itemとsecond_itemsを組み合わせて結果を表示する
    combined_list = []
    # second_itemsのリストが存在するか、またはNoneであるかをチェック
    combined_second = updated_second_items[i] if i < len(updated_second_items) else None

    # 組み合わせをリストに追加
    combined = {"first": first_item[i], "second": combined_second}
    combined_list.append(combined)

    # 結果の印刷
    for first_second_joinitem in combined_list:#★
    # item['first']のスペースまでの文字を抽出
        first_part = ""
        clean_text = str(first_second_joinitem['first']).replace("</br>", "")#★
    if "," in clean_text:
        pattern = ',(\d|,)*(?=\s|$)' # 「,」の後に(「数字」か「,」)の場合
        # 条件に一致するかチェック
        if re.search(pattern, clean_text):
            first_part = clean_text.split(" ")[0]
        else:
            sub_pattern = r'[A-Za-z0-9/ /]'
            # 置換処理を行い、日本語のみ抽出
            result = re.sub(sub_pattern, '', clean_text)
            first_part = result  # 数字、アルファベット、コンマを削除
    else:
        first_part = clean_text.split(" ")[0]

    # item['second']を置換
    second_parts = []
    if first_second_joinitem['second'] is not None:#★
        for element in first_second_joinitem['second']:#★
            if element in replacement_patterns:
                second_parts.append(replacement_patterns[element])
            else:
                second_parts.append(element)

    # second_partsが複数要素を持つ可能性も考えられるので、','.join()で文字列に変換
    second_part_joined = ', '.join(second_parts)

    # 結果の表示
    if first_second_joinitem['second'] == None: # 損傷種類がNoneのとき
        combined_data = None
    elif len(second_items[i]) == 1:
        combined_data = f"{first_part}に{second_part_joined}が見られる。"
    else:
        item_str = ', '.join(second_items[i]) # ['①腐食-b']を①腐食-bに変更
        start_special_text = item_str.find(",")+1 # 最初のコンマ位置を検索
        combined_data = f"{first_part}に{second_part_joined}が見られる。\n【関連損傷】\n{item_str[start_special_text:]}"
        # \n文字列のときの改行文字
    items = {'first': first_item[i], 'second': second_items[i], 'third': third, 'last': picture_urls, 'picture': 'infra/noImage.png', 'textarea_content': combined_data, 'damage_coordinate': damage_coordinate[i], 'picture_coordinate': picture_coordinate[i]}
