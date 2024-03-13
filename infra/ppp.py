picture = "9月7日 S628 前-15"

picture_name = picture.replace(" ", "　").replace("S", "佐藤")
# 小文字を大文字に変換
print(picture_name)

print(picture_name.find("　"))
# 最初のスペース位置を検索

print(len(picture_name))
# 文字数

print(picture_name[0:picture_name.find("　")])
# 最初のスペース位置まで抽出

print(picture_name.find("　", picture_name.find("　") + 1))
# 次のスペース位置まで抽出

print(picture_name[picture_name.find("　")+1:picture_name.find("　", picture_name.find("　") + 1)])
# 最初のスペース位置から次のスペース位置まで抽出

print(picture[0:picture.find(" ")+2].replace("S", "佐藤"))
print(picture[picture.find(" ")+2:picture.find(" ", picture.find(" ") + 1)])



