from django.contrib import admin
from .models import Approach, Infra, Table, Article, CustomUser, LoadGrade, LoadWeight, Regulation, Rulebook, Thirdparty, UnderCondition, PartsNumber, NameEntry
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
admin.site.register(Table) # 損傷写真帳
admin.site.register(PartsNumber) # 番号登録
admin.site.register(NameEntry) # 名前とアルファベットの紐付け