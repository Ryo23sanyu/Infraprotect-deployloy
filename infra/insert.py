import re

text = [['※特記なき損傷'], ['横桁 Cr0102 ①-d'], ['横桁 Cr0201,0301,0402 ⑦-d'], ['床版 Ds0101～0108 ⑪-c'], \
  ['縦桁 Mg0101～0108,0201～0208 ①-d'], ['主桁 Mg0101～0208 ①-d'], ['横桁 Cr0101,0201,0301'], ['対傾構 Cf0102,0202,0302 ①-d'],\
    ['防護柵 Gf0101,0401'],['地覆 Fg0101,0401'],['縁石 Cu0201,0301 ㉓-c']]

#text = [['主桁 Mg0101 ②-e'],['縦桁 St0101 ①-c'],['横桁 Cr0101'],['下横構 Ll0101 ①-d'],['防護柵 Gf0101'],['地覆 Fg0101 ㉓-c']]

pattern = r"\s[\u2460-\u3256]"
# 正規表現パターン（\s:スペース,\d:数字,\u2460-\u3256:①～㉖）をpattern変数に代入

# リストを逆順でループし、条件に応じて処理
for i in range(len(text)-1, -1, -1):  # 後ろから前にループ
    item = text[i][0]  # textリストの各サブリストの最初の要素（[0]）をitem変数に代入（地覆 ㉓-c）
    if item.startswith("※"):
      text.remove(text[i]) # 配列から除外する
    elif re.search(pattern, item):  # itemが正規表現patternと一致している場合（スペース丸数字の並びがある）
        last_found = item  # last_found変数にitem要素を代入（地覆 ㉓-c）
        # print(last_found) 丸数字が付いている要素のみ出力
    else: # itemが正規表現patternと一致していない場合（スペース丸数字の並びがない）
        if 'last_found' in locals():  # last_foundが定義されている（要素が代入されている）場合のみ
            space = last_found.replace("　", " ")
            # 大文字スペースがあれば小文字に変換
            second = space.find(" ", space.find(" ") + 1)#10
            # 2つ目のスペース位置まで抽出
            text[i][0] = item + last_found[second-1:]
            # item:スペース丸数字の並びがない文字列
            # last_found:スペース丸数字の並びがある文字列
            # len(item):item（横桁 Cr0101の場合、9文字）の文字数
            # last_found[len(item):]:スペース丸数字の並びが、ある文字数からない文字数を引いた後の文字
            
            #print(len(item)) # 10 / 9
            #print(item) # 防護柵 Gf0101 / 横桁 Cr0101
            #print(last_found) # 地覆 Fg0101 ㉓-c / 下横構 Ll0101 ①-d
            #print(last_found[len(item):]) # ㉓-c / 1 ①-d

print(text)