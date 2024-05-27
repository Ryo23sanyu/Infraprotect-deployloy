def replace_string(input_string, replacement_patterns):
    for old, new in replacement_patterns.items():
        input_string = input_string.replace(old, new)
    return input_string

# 例：
replacement_patterns = {
    'foo': 'bar',
    'hello': 'hi',
    'world': 'earth'
}

input_string = "hello, world! foo is here."
output_string = replace_string(input_string, replacement_patterns)

print(output_string)  # 結果: "hi, earth! bar is here."