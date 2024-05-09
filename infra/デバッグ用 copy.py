import glob
import re
from markupsafe import Markup

extracted_text = [['横桁 Cr0803', '⑦剥離・鉄筋露出-d', '写真番号-15', '9月7日 S458(前-8)', ['543207.0862507953', '218366.5575399188'], ['545418.5774821687', '218368.3759352968']], ['主桁 Mg0901', '⑰その他(分類6:異物混入)-e', '写真番号-2', '9月7日 S404(前-1)', ['532240.3861927793', '218366.5575399188'], ['534192.8564975171', '218396.3930096343']], ['横桁 Cr0201,0301,0402,0403,0602,0604,0704', '⑦剥離・鉄筋露出-d'], ['床版 Ds0201,0203', '⑦剥離・鉄筋露出-d'], ['排水管 Dp0201,0202', '①腐食(小大)-c,⑤防食機能の劣化(分類1)-e'], ['横桁 Cr0801', '⑦剥離・鉄筋露出-d', '写真番号-12', '9月7日 S525(前-3)', ['527566.5420863405', '220430.3566962297'], ['527793.2963477422', '220070.4196068052']], ['排水管 Dp0101', '①腐食(大大)-e', '⑤防食機能の劣化(分類1)-e', '写真番号-31', '9月7日 S422(前-23)', ['538482.3557216563', '229268.8593029478'], ['538810.3087944178', '228910.3502713814']], ['横桁 Cr0802', '⑦剥離・鉄筋露出-d', '写真番号-13,14', '9月7日 S396,S412(前-4)', ['538443.3187868086', '218366.5575399188'], ['538761.6085522854', '218087.1577589952']], ['床版 Ds0803', '⑦剥離・鉄筋露出-d', '写真番号-17', '9月7日 S465(前-12)', ['544955.785269761', '220430.3566962297'], ['545192.2035962', '220088.065259854']], ['横桁 Cr0503', '⑦剥離・鉄筋露出-d', '⑰その他(分類6:施工不良)-e', '写真番号-10,11', '9月7日 S450,S452(前-6,7)', ['546181.340571892', '222553.0807470059'], ['546769.9402349197', '222164.8389810835']], ['横桁 Cr0401', '⑦剥離・鉄筋露出-e', '写真番号-9', '9月7日 S523(前-2)', ['529221.0193919685', '223295.995449547'], ['529401.0143646629', '222981.8261548198']], ['床版 Ds0101', '⑦剥離・鉄筋露出-d', '写真番号-16', '9月7日 S497(前-11)', ['531595.7611265536', '227530.3566962298'], ['531805.9667048807', '227218.1705246582']]]

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
print(len(first_item))

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

print(len(second_items))

# 最後から2番目の要素を抽出（写真番号-00）
third_items = [sub_list[-4] if len(sub_list) >= 5 else '' for sub_list in extracted_text]
print(len(third_items))

# 最後の要素を抽出（Defpoints）
bottom_item = [sub_list[-3] if len(sub_list) >= 4 else '' for sub_list in extracted_text]
print(len(bottom_item))

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

    # print(item) # ✕： 438.jpg
    
    bridge = {
        "first": first_item[i],
        "second": second_items[i]
    }

    # 抽出・置換ロジックをここに実装
    first_part_extracted = bridge["first"][:bridge["first"].find(" ")]
    
    # bridge.secondをどのように置換するかのロジック
    replacement_patterns = {
        "①腐食(大大)-e": "板厚減少を伴う腐食",
        "⑦剥離・鉄筋露出-c": "コンクリートの剥離",
        "⑦剥離・鉄筋露出-d": "鉄筋露出",
        "⑦剥離・鉄筋露出-e": "著しい鉄筋露出",
        "⑳漏水・滞水-e": "著しい鉄筋露出",
    }
    
    
    # << ①と⑤があるとき、⑤を消す >>
    for sublist in second_items:
    # リスト内の要素を走査して、先頭が「①」の要素が存在するかチェックする
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

    second_replaced = "、".join(replacement_patterns.get(item, item) for item in sublist)
    print(first_part_extracted + "に" + second_replaced + "が見られる。")