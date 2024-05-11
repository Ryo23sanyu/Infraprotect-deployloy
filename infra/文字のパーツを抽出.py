picture = "9月7日 S628 前-15"

picture_name = picture.replace(" ", "　").replace("S", "佐藤")
# 小文字を大文字に変換
print(picture_name)

print(picture_name.find("　"))
# 最初のスペース位置を検索

print(len(picture_name))
# 文字数

print(picture_name[:picture_name.find("　")])
# 最初のスペース位置まで抽出

print(picture_name.find("　", picture_name.find("　") + 1))
# 次のスペース位置まで抽出

print(picture_name[picture_name.find("　")+1:picture_name.find("　", picture_name.find("　") + 1)])
# 最初のスペース位置から次のスペース位置まで抽出

print(picture[0:picture.find(" ")+2].replace("S", "佐藤"))
print(picture[picture.find(" ")+2:picture.find(" ", picture.find(" ") + 1)])



last_item = ['NON-a', '9月7日 S*/*404', '9月7日 S*/*537', '9月8日 S*/*117,9月8日 S*/*253']

for index, value in enumerate(last_item):
    if value == 5:
        last_item[index] = 9

target_file = [last_item + '.jpg' for last_item in last_item]

print(target_file) # ['NON-a.jpg', '9月7日 S*/*404.jpg', '9月7日 S*/*537.jpg', '9月8日 S*/*117,9月8日 S*/*253.jpg']

s = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(s[5]) # F
print(s[:-1]) # ABCDEFGHIJKLMNOPQRSTUVWXY

