from django.http import HttpResponse# 追加
def sample_view(request):# 追加
    start = "0101"
    end = "0206"

# 最初の2桁と最後の2桁を取得
    start_prefix = start[:2]
    start_suffix = start[2:]
    end_prefix = end[:2]
    end_suffix = end[2:]

# 抽出した数字を表示
    result = ""# 追加
    for prefix in range(int(start_prefix), int(end_prefix)+1):
        for suffix in range(int(start_suffix), int(end_suffix)+1):
            result += "{:02d}{:02d}".format(prefix, suffix)
        
    return HttpResponse(result)# 追加