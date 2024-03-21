last_item_replaced = [['None'], ['9月7日\u3000佐藤*/*537.jpg'], ['9月8日\u3000佐藤*/*117.jpg,9月8日\u3000佐藤*/*253.jpg']]

last = []
for picture_text_list in last_item_replaced:
  for picture_text in picture_text_list:
    if "," in picture_text:
        dis_items = picture_text.split(',') # 「9月8日 S*/*117」,「9月8日 S*/*253」
        sub_dis_items = ["sample" + dis_item for dis_item in dis_items] # リスト型に文字を追加する方法
        join_dis_items = ",".join(sub_dis_items)# 加工した内容をカンマ区切りの１つの文字列に戻す
        last.append(join_dis_items)
    else:
        new = "sample" + picture_text
        last.append(new)

print(last)