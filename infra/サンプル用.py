import re

bridge = "横桁 Cr0304　⑦剥離・鉄筋露出-e：1径間　(横桁 Cr04/⑦剥離・鉄筋露出-e/1径間)"

def initial_segment(value):
    """スペースまでの文字列を抽出"""
    match = re.match(r'^[^　]+', value)
    return match.group(0) if match else ''

print(initial_segment(bridge))
