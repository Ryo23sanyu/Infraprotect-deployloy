from django.contrib import admin
from .models import Approach, Infra, Article, CustomUser, LoadGrade, LoadWeight, Regulation, Rulebook, Thirdparty, UnderCondition
from django.contrib.auth.admin import UserAdmin

# models.pyのclass名とカッコの中を合わせる
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Infra) # 橋梁
admin.site.register(Article) # 案件
admin.site.register(Regulation) # 道路規制
admin.site.register(LoadWeight) # 活荷重
admin.site.register(LoadGrade) # 等級
admin.site.register(Rulebook) # 適用示方書
admin.site.register(Approach) # 近接方法
admin.site.register(Thirdparty) # 第三者点検の有無
admin.site.register(UnderCondition) # 路下条件