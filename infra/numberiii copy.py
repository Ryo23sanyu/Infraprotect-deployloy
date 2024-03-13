top_item = ['9月7日 S1', '9月8日 S6,S7', '9月17日 S6,9月7日 S2,S8']
new_text = []

splited_text = top_item.split(',')
for item in splited_text:
  new_text.append(item)    

for item in top_item:
    if "," in item:
        for j in range(len(item)-1):
            if item[j] == "," and item[j+1].isalpha():#「,」の次がアルファベットの場合
                for s in range(len(item)-1):
                    if item[s] == " ":
                        print(item[:s+1])#舗装 Pm
                        print(item[s+1:])#0101,0201
                        new_text.append(item[:item.find(",")+1] + item[:s+1] + item[item.find(",")+1:])
                        break
    else:
        new_text.append(item)

print(new_text)