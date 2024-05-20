import glob
import re

from markupsafe import Markup

extracted_text = [['横桁 Cr0803', '⑦剥離・鉄筋露出-d', '写真番号-15', '9月7日 S458(前-8)', ['543207.0862507953', '218366.5575399188'], ['545418.5774821687', '218368.3759352968']], ['主桁 Mg0901', '⑰その他(分類6:異物混入)-e', '写真番号-2', '9月7日 S404(前-1)', ['532240.3861927793', '218366.5575399188'], ['534192.8564975171', '218396.3930096343']], ['横桁 Cr0201,0301,0402,0403,0602,0604,0704', '⑦剥離・鉄筋露出-d', ['525003.839727268', '214191.031706055']], ['床版 Ds0201,0203', '⑦剥離・鉄筋露出-d', ['525003.839727268', '214191.031706055']], \
    ['排水管 Dp0201,0202', '①腐食(小大)-c,⑤防食機能の劣化(分類1)-e', ['525003.839727268', '214191.031706055']], ['横桁 Cr0801', '⑦剥離・鉄筋露出-d', '写真番号-12', '9月7日 S525(前-3)', ['527566.5420863405', '220430.3566962297'], ['527793.2963477422', '220070.4196068052']], ['排水管 Dp0101', '①腐食(大大)-e', '⑤防食機能の劣化(分類1)-e', '写真番号-31', '9月7日 S422(前-23)', ['538482.3557216563', '229268.8593029478'], ['538810.3087944178', '228910.3502713814']], \
        ['横桁 Cr0802', '⑦剥離・鉄筋露出-d', '写真番号-13,14', '9月7日 S396,S412(前-4)', ['538443.3187868086', '218366.5575399188'], ['538761.6085522854', '218087.1577589952']], ['床版 Ds0803', '⑦剥離・鉄筋露出-d', '写真番号-17', '9月7日 S465(前-12)', ['544955.785269761', '220430.3566962297'], ['545192.2035962', '220088.065259854']], ['横桁 Cr0503', '⑦剥離・鉄筋露出-d', '⑰その他(分類6:施工不良)-e', '写真番号-10,11', '9月7日 S450,S452(前-6,7)', ['546181.340571892', '222553.0807470059'], ['546769.9402349197', '222164.8389810835']], ['横桁 Cr0401', '⑦剥離・鉄筋露出-e', '写真番号-9', '9月7日 S523(前-2)', ['529221.0193919685', '223295.995449547'], ['529401.0143646629', '222981.8261548198']], ['床版 Ds0101', '⑦剥離・鉄筋露出-d', '写真番号-16', '9月7日 S497(前-11)', ['531595.7611265536', '227530.3566962298'], ['531805.9667048807', '227218.1705246582']], ['横桁 Cr0102', '⑰その他(分類6:施工不良)-e', '写真番号-4,5', '9月7日 S424,S430', ['532578.7587482664', '229268.8593029478'], ['532985.6409545547', '228954.2335446222']], ['横桁 Cr0103', '⑦剥離・鉄筋露出-e', '写真番号-6', '9月7日 S433(前-5)', ['543427.3505810621', '229268.8593029478'], ['543666.8474364146', '228932.0443462149']], \
            ['排水管 Dp0102', '①腐食(小大)-c', '⑤防食機能の劣化(分類1)-e', '写真番号-32', '9月7日 S486(前-24)', ['547059.1990495767', '229268.8593029478'], ['549204.9604817769', '229256.3408485695']], ['横桁 Cr0304', '⑦剥離・鉄筋露出-e', '写真番号-8', '9月7日 S476(前-10)', ['547430.0305409065', '224715.8752162406'], ['547714.7833405402', '224403.0381771689']], ['横桁 Cr0204', '⑦剥離・鉄筋露出-e', '写真番号-7', '9月7日 S478(前-9)', ['548316.6020528428', '226251.4621194576'], ['549169.7165741528', '225941.858472284']], ['横桁 Cr0101', '⑰その他(分類6:施工不良)-e', '写真番号-3', '9月7日 S496', ['529717.5478308655', '226255.0784977268'], ['530492.2250104588', '225969.2279711204']], \
    ['主桁 Mg0901', '⑦剥離・鉄筋露出-c', '写真番号-1', '9月7日 S537', ['528508.2182060345', '218366.5575399188'], ['529225.1221130126', '218048.3941777406']], ['地覆 Fg0201', '⑫うき-e', '写真番号-24', '9月7日 S535(前-17)', ['529523.5331537114', '216164.654853505'], ['529841.2180579801', '215806.1718362219']], ['橋台[胸壁] Ap0102,橋台[竪壁] Ac0102,伸縮装置 Ej0102', '⑳漏水・滞水-e', '写真番号-19', '9月7日 S443(前-14)', ['534633.1754138757', '198400.9331532792'], ['537045.4396522791', '198420.7293499758']], ['橋台[胸壁] Ap0101,橋台[竪壁] Ac0101,伸縮装置 Ej0101', '⑳漏水・滞水-e', '写真番号-18', '9月7日 S438(前-13)', ['535305.6406762057', '190342.4721676922'], ['537494.8440878117', '190371.7813098583']], \
        ['排水ます Dr0101', '⑰その他(分類6:埋没)-e', '写真番号-30', '9月7日 S617(前-22)', ['533244.2054744802', '169468.5013850681'], ['535267.305622106', '169437.0789344727']], ['防護柵 Gf0101', '⑦剥離・鉄筋露出-d', '写真番号-21', '9月7日 S587(前-15)', ['546386.0254916904', '168103.8976152274'], ['547193.0579465147', '167783.5999853493']], \
            ['防護柵 Gf0101', '⑦剥離・鉄筋露出-c', '写真番号-20', '9月7日 S591', ['544240.5351249668', '169468.5013850681'], ['544570.7952826328', '169116.7615150949']], ['防護柵 Gf0101', '⑦剥離・鉄筋露出-d', '写真番号-22', '9月7日 S620', ['538818.4080393101', '169468.5013850681'], ['539306.9846939673', '169153.6834979908']], ['舗装 Pm0101', '㉔土砂詰まり-e', '写真番号-26', '9月7日 S596(前-18)', ['533352.4944797055', '168103.8976152274'], ['533703.9706752875', '167792.7034569031']], ['防護柵 Gf0201', '⑦剥離・鉄筋露出-c', '写真番号-23', '9月7日 S637(前-16)', ['528542.6628878898', '157981.6059456724'], ['528817.9756552395', '157621.3087358776']], ['舗装 Pm0201', '㉔土砂詰まり-e', '写真番号-29', '9月7日 S646(前-21)', ['528784.5220314491', '161131.0756502239'], ['528891.6020477654', '160767.6558934028']], ['舗装 Pm0201', '⑮舗装の異常-e', '写真番号-28', '9月7日 S646(前-20)', ['540139.0897682087', '157981.6059456724'], ['542213.8022292339', '158011.4174302613']], ['舗装 Pm0201', '⑮舗装の異常-e', '写真番号-27', '9月7日 H259(前-19)', ['545103.73998104', '161131.0756502239'], ['547126.0496139134', '161150.7776329561']], ['舗装 Pm0101,0201', '⑮舗装の異常-e', '写真番号-25', '9月7日 S616', ['530200.056550543', '165764.7673630748'], ['530448.4275586283', '165439.1406174743']], \
                ['支承本体 Bh0102,沓座モルタル Bm0102', 'NON-a', ['530448.4275586283', '165439.1406174743']], ['PC定着部 Cn1203', 'NON-a', ['530448.4275586283', '165439.1406174743']], ['排水ます Dr0102,0201,0202', '⑰その他(分類6:埋没)-e', ['525003.839727268', '156577.5780402338']]]

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
        
# << ◆写真メモを作成するコード◆ >>
    bridge_damage = [] # すべての"bridge"辞書を格納するリスト

    bridge = {
        "first": first_item[i],
        "second": second_items[i] if i < len(second_items) else None  # second_itemsが足りない場合にNoneを使用
    }
    bridge_damage.append(bridge)
    #print(bridge)

    replacement_patterns = {
        "①腐食(小小)-b": "腐食", # 1
        "①腐食(小大)-c": "拡がりのある腐食",
        "①腐食(大小)-d": "板厚減少を伴う腐食",
        "①腐食(大大)-e": "板厚減少を伴う拡がりのある腐食",
        "③ゆるみ・脱落-c": "ボルト、ナットにゆるみ・脱落（●本中●本）",
        "③ゆるみ・脱落-e": "ボルト、ナットにゆるみ・脱落（●本中●本）", # 3
        "④破断-e": "鋼材の破断", # 4
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

    pavement_items = []
    for damage_parts in bridge_damage:
        if isinstance(damage_parts["second"], list):
            filtered_second_items = []
            for second_list_item in damage_parts["second"]:
                if any(d.startswith('①') for d in second_list_item if isinstance(d, str)):
                    filtered_second_items.append([d for d in second_list_item if not d.startswith('⑤')])
                else:
                    filtered_second_items.append(second_list_item)
            damage_parts["second"] = filtered_second_items  # フィルタリング後の second_items をセット
        pavement_items.append(damage_parts)

    def update_items(items):
        new_items = []
        for item in items:
            if isinstance(item, list):
                new_items.append(update_items(item))
            elif isinstance(item, str):
                if item.startswith('⑰'):
                    match = re.search(r'(?<=:)(.*?)(?=\)-e)', item)
                    if match:
                        new_items.append(match.group(1))
                    else:
                        new_items.append(item)
                else:
                    new_items.append(item)
        return new_items

    updated_second_items = update_items(damage_parts["second"])
                
    # << ◆まだ◆ >>
    combined_list = []
    if damage_parts["second"] is not None:
        combined_second = updated_second_items #if i < len(updated_second_items) else None
    else:
        combined_second = None
    
    combined = {"first": first_item[i], "second": combined_second}
    combined_list.append(combined)
    #print(combined_list)

# << 損傷メモの作成 >>
    # 部材名を表示
    for first_second_joinitem in combined_list:#★
        #print(first_second_joinitem)
        # item['first']のスペースまでの文字を抽出
        first_part = ""
        clean_text = str(first_second_joinitem['first']).replace("</br>", "")#★
        #print(clean_text)
        markup_pattern = re.compile(r"Markup\('([^']+)'\)")# 正規表現でMarkupの要素部分を抽出
        
        def extract_before_space(text):
            return text.split(' ')[0]# スペースより前の部分を抽出
        
        # 要素を分割する
        parts = re.findall(markup_pattern, clean_text)
        # 各要素のスペースより前の部分を抽出
        first_part = [extract_before_space(part) for part in parts]
        #print(parts)     
        
        # item['second']を置換        
        second_parts = []
        if first_second_joinitem['second'] is not None:#★
            for element in first_second_joinitem['second']:#★
                for part_element in element:
                    if part_element in replacement_patterns:
                        second_parts.append(replacement_patterns[part_element])
                    else:
                        second_parts.append(part_element)

        # second_partsが複数要素を持つ可能性も考えられるので、','.join()で文字列に変換
        second_part_joined = ', '.join(second_parts)
        # 損傷名をコンマでつなげる
        join_damagename_result = [",".join(join_damagename_sublist) for join_damagename_sublist in second_items[i]]


        # 準備したfirst_part（部材名）とsecond_part_joined（損傷名）の合体
        if second_items[i] is None: # 損傷種類がNoneのとき
            combined_data = None # 損傷メモはNone
        else:
            parts_item_str = ','.join(first_part) # リストから文字列に変換
            special_text = '' # デフォルトの特別テキストは空文字列

            if len(second_items[i]) == 1: # 損傷種類が1つにまとまっている場合
                for result in join_damagename_result:
                    if "," in result:
                        memo_special_text = result.find(",") + 1  # 最初のコンマ位置を検索してその次の文字位置を取得
                        special_text = f"\n【関連損傷】\n{result[memo_special_text:]}"
                        break

                combined_data = f"{parts_item_str}に{second_part_joined}が見られる。{special_text}"
                #print(combined_data)
                #print(" ")
                
            else: # 複数部材で異なる損傷がある場合
                # 先頭の部分（主桁）のテキスト
                changed_damage_name = []
                # 置換パターンに基づいて置換する関数を定義
                def replace_patterns(text, patterns):
                    for old, new in patterns.items():
                        text = text.replace(old, new)
                    return text

                # 各ダメージ名を置換
                for damage in join_damagename_result:
                    changed_damage_name.append(replace_patterns(damage, replacement_patterns))

                # 先頭の部分（主桁）のテキスト
                combined_result = f"{first_part[0]}に{changed_damage_name[0]}が見られる。"

                combined_result += f"また、{first_part[1]}に{changed_damage_name[1]}"

                # 2つ目以降の要素を結合
                if len(first_part) >= 3:
                    for i in range(2, len(first_part)):
                        combined_result += f"、{first_part[i]}に{changed_damage_name[i]}"
                else:
                    None

                if len(first_part) >= 2:
                    combined_result += "が見られる。"

                # 1つ目の要素にカンマがあるかどうかをチェック
                if "," in join_damagename_result[0]:
                    # カンマがある場合、1つ目のpartsと1つ目のjoin_damagename_resultを結合し、残りはそのまま結合
                    tokki_1 = f"\n【関連損傷】\n{parts[0]}:{join_damagename_result[0]}"
                    for i in range(1, len(parts)):
                        tokki_1 += f"、{parts[i]}:{join_damagename_result[i]}"
                else:
                    # カンマがない場合、2つ目以降のpartsとjoin_damagename_resultを結合
                    tokki_1 = "\n【関連損傷】\n"
                    for i in range(len(parts)):
                        if i > 0:
                            if tokki_1:
                                tokki_1 += ""
                            tokki_1 += f"{parts[i]}:{join_damagename_result[i]}、"
                combined_result += tokki_1
                combined_data = combined_result[:-1]
                

            # \n文字列のときの改行文字
        items = {'first': first_item[i], 'second': second_items[i], 'third': third, 'last': picture_urls, 'picture': 'infra/noImage.png', 'textarea_content': combined_data, 'damage_coordinate': damage_coordinate[i], 'picture_coordinate': picture_coordinate[i]}
        print(f"first_part {first_part}")

# << ◆ここまでは反映済み◆ >>
        #優先順位の指定
        order_dict = {"主桁": 1, "横桁": 2, "床版": 3, "PC定着部": 4, "橋台[胸壁]": 5, "橋台[竪壁]": 6, "支承本体": 7, "沓座モルタル": 8, "防護柵": 9, "地覆": 10, "伸縮装置": 11, "舗装": 12, "排水ます": 13, "排水管": 14}
        order_number = {"None": 0, "①": 1, "②": 2, "③": 3, "④": 4, "⑤": 5, "⑥": 6, "⑦": 7, "⑧": 8, "⑨": 9, "⑩": 10, "⑪": 11, "⑫": 12, "⑬": 13, "⑭": 14, "⑮": 15, "⑯": 16, "⑰": 17, "⑱": 18, "⑲": 19, "⑳": 20, "㉑": 21, "㉒": 22, "㉓": 23, "㉔": 24, "㉕": 25, "㉖": 26}
        order_lank = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
        
        def sort_category(text): # sort_category関数を定義
            # テキストがリスト形式で渡される場合を想定
            if isinstance(text, list) and len(text) > 0:
                first_part = text[0]  # リストの最初の要素を取得
            else:
                first_part = text  # それ以外の場合はそのまま使用
            for key, val in order_dict.items(): # keyがキー(主桁～防護柵)、valが値(1～6)
                if str(first_part).startswith(key): # textの1文字目がキー(主桁～防護柵)の場合
                    return val # 値(1～6)を返す
            return max(order_dict.values()) + 1
            
# 文字列から数値部分だけを抽出してリストに格納する
        def extract_numbers(s):
            # 文字列をカンマで分割してリストにする
            if "," in item:
                parts = [item.split(',') for item in s]
            else:
                parts = item
            # 抽出された数値部分を格納するリスト
            numbers = []
            # カンマで分割した各部分について処理を行う
            for part in parts:
                # 各部分から数字だけを抽出する
                digit_str = ''.join(filter(str.isdigit, part))
                # 抽出された数字部分が空でない場合
                if digit_str:
                    # 数字部分を整数に変換してリストに追加する
                    number = int(digit_str)
                    numbers.append(number)
            return numbers

        def get_first_key(first):
            num_parts = extract_numbers(first)
            # 数値が含まれていない場合は、ソートで最後になるような大きな値を返す
            return min(num_parts) if num_parts else float('inf')

        def sort_number(second_list):
            # リストが空の場合の処理
            if not second_list or len(second_list) == 0:  # 条件式の調整
                return max(order_number.values()) + 1
            else:
                second_text = second_list[0]
                if "-" in second_text: #second_textの文字の中に-があるとき
                    num_text = second_text[0] #num_textにsecond_textの1文字目を入れる
                    for key, val in order_number.items():
                        if num_text.startswith(key):
                            return val #数字を返す
            return max(order_number.values()) + 1 #リストの最大数+1の数字を返す

        def sort_lank(second_list):
            if not second_list or len(second_list) == 0:  # 条件式の調整
                return max(order_number.values()) + 1
            else:
                second_text = second_list[0]
                if '-' in second_text:
                    lank_text = second_text.split("-")[1]
                    for key, val in order_lank.items():
                        if lank_text.startswith(key):
                            return val
                return max(order_lank.values()) + 1

        damage_table.append(items)
sorted_text_list = sorted(damage_table, key=lambda text: (sort_category(text['first']), get_first_key(text['first']), sort_number(text['second']), sort_lank(text['second'])))
print(sorted_text_list)