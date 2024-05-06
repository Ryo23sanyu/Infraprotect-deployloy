import re

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

# 仮想の `extracted_text` リスト
extracted_text = [["hello,world,this,is,a,test,string,with,several,commas,"]]

# 指定された条件で処理を行う
first_item = [insert_line_breaks_on_commas(sub_list[0]) for sub_list in extracted_text]

print(first_item)
