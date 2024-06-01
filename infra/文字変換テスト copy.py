import re

request_list = {'first': [['主桁 Mg0901']], 'second': [['⑰その他(分類6:異物混入)-e']]}

test = request_list['second'][0]

# 先頭が文字（日本語やアルファベットなど）の場合
def all_match_condition(lst):
    """
    リスト内のすべての項目が特定条件に一致するか確認します。
    ただし、空のリストの場合、Falseを返します。
    """
    # 空のリストの場合は False を返す
    if not lst:
        return False
    
    pattern = re.compile(r'\A[^\W\d_]', re.UNICODE)
    return all(pattern.match(item) for item in lst)

if all_match_condition(test):
    print(request_list)
else:
    request_list['second'] = [request_list['second']]
    print(request_list)