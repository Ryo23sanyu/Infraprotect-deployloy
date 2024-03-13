def process_string(input_string):
    # 文字列をスペースで分割して、各要素を配列に格納する
    elements = input_string.split(" ")

    # 要素の数だけループする
    for i in range(len(elements)):
        # アルファベットが含まれているかどうかを判定する
        if any(c.isalpha() for c in elements[i]):
            # アルファベットが含まれている場合は、",”の直前までの文字列に置き換える
            elements[i] = input_string[:input_string.find(",")+1]
        else:
            # アルファベットが含まれていない場合は、",”の直後の文字列に置き換える
            elements[i] = input_string[input_string.find(",")+1:]

    # 結果を結合して返す
    result = " ".join(elements)
    return result