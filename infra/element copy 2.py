top_item = ['NON-a', '⑤-e', '⑦-d⑧-d', '⑦-d⑧-d⑪-d']
new_text = []

for item in top_item:
        for s in range(len(item)-1):
            if item[s] in "abcde" and item[s+1] in "①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳㉑㉒㉓㉔㉕㉖":
                print(item[:s+1])#舗装 Pm
                print(item[s+1:])#0101,0201
                new_text.append(item[:s+1] + "</br></br>" + item[s+1:])
                break
        else:
            new_text.append(item)

print(new_text)