s = "舗装 Pm0101,0201"

elements = s.split(",")

new_elements = []
for i, element in enumerate(elements):
    if i > 0:
        # 前の要素の最初からスペースの位置までをコピーする
        previous_element = elements[i-1].split()[0]
        new_element = previous_element + " " + element
    else:
        new_element = element
    new_elements.append(new_element)

result = ",".join(new_elements)

print(result)