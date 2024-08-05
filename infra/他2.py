import difflib

# 初期テキスト
text_1 = "主桁に鉄筋露出が見られる。状況に応じて補修が必要である。"
text_2 = "主桁に鉄筋露出が見られる。予防保全の観点から、補修が必要である。"
text_3 = "主桁隅角部に鉄筋露出が見られる。損傷は軽微なため、補修が必要と考える。"

# 差分を取得する関数
def get_diff(text_from, text_to):
    seqm = difflib.SequenceMatcher(None, text_from, text_to)
    diffs = []
    for opcode in seqm.get_opcodes():
        if opcode[0] != "equal":  # 変更がある部分のみ
            diffs.append(opcode)
    return diffs

# 差分を適用する関数
def apply_diff(text, diffs, text_from, text_to):
    new_text = text
    offset = 0
    for tag, i1, i2, j1, j2 in diffs:
        if tag in ["replace", "delete"]:
            new_text = new_text[:i1 + offset] + text_to[j1:j2] + new_text[i2 + offset:]
            offset += (j2 - j1) - (i2 - i1)
        elif tag == "insert":
            new_text = new_text[:i1 + offset] + text_to[j1:j2] + new_text[i1 + offset:]
            offset += (j2 - j1)
    return new_text

# text_1とtext_3の差分を取得
diffs = get_diff(text_1, text_3)

# text_2に同じ変更を適用
text_4 = apply_diff(text_2, diffs, text_1, text_3)

print("Original text_2:", text_2)
print("Edited text_4:", text_4)
