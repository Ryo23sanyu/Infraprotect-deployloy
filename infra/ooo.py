picture = "9月7日 S628 前-15"

result = ""
for i in range(len(picture)-1):# 文字数-1回
    if picture[i].isascii() and picture[i+1].isdigit():#.isascii():英語のときTrue、.isdigit():数字のときTrue
        result = picture[:i+1]
        break

print(result)

