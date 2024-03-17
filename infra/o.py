import glob
import re


text_items = ['NON-a', '9月7日 S404(前-1)', '9月7日 S537', '9月8日 S117(前-3),9月8日 S253']
damage_table = []

result_items = []# 配列を作成
for item in text_items:# text_itemsの要素を1つずつitem変数に入れてforループする
    if ',' in item:# 要素の中にカンマが含まれている場合に実行
        sub_items = item.split(',')# カンマが含まれている場合カンマで分割
        extracted_item = []# 配列を作成
        for item in sub_items:# bottom_itemの要素を1つずつitem変数に入れてforループする
            for i in range(len(item)):#itemの文字数をiに代入
                if "A" <= item[i].upper() <= "Z" and i < len(item) - 1 and item[i+1].isnumeric():#i文字目がアルファベットかつ、次の文字が数字の場合
                    extracted_item.append(item[:i+1]+"*/*"+item[i+1:])# アルファベットと数字の間に*/*を入れてextracted_itemに代入
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
    pattern = re.compile(r"\([^()]*\)")# ()で囲まれた文字を抽出
    result = [pattern.sub("", string) for string in last]# 抽出した文字を空文字に置換
    return result

last = result_items
last_item = remove_parentheses_from_list(last)

last_item_replaced = []
for item in last_item:
    if item == "NON-a":
        last_item_replaced.append(item.replace("S", "佐藤").replace("H", "濵田").replace(" ", "　"))
    elif "," in item: # 「9月8日 S*/*117,9月8日 S*/*253」
        #last_item_replaced.append(item.replace("S", "佐藤").replace("H", "濵田") + ".jpg")
        dis_items = item.split(',') # 「9月8日 S*/*117」,「9月8日 S*/*253」
        sub_dis_items = [dis_item + ".jpg" for dis_item in dis_items] # リスト型に文字を追加する方法
        join_dis_items = ",".join(sub_dis_items)# 加工した内容をカンマ区切りの１つの文字列に戻す
        last_item_replaced.append(join_dis_items.replace("S", "佐藤").replace("H", "濵田").replace(" ", "　"))# result_itemsに格納
    else:
        last_item_replaced.append(item.replace("S", "佐藤").replace("H", "濵田").replace(" ", "　") + ".jpg")
    
print(last_item_replaced)