from django.contrib import admin
from django.db import models

from infra.forms import PartsNumberForm
from .models import Approach, DamageComment, DamageList, FullReportData, Infra, Material, PartsName, Table, Article, CustomUser, LoadGrade, LoadWeight, Regulation, Rulebook, Thirdparty, UnderCondition, PartsNumber, NameEntry
from django.contrib.auth.admin import UserAdmin
from django.db.models import Case, When, Value, IntegerField

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
admin.site.register(PartsName) # 番号登録
admin.site.register(PartsNumber) # 番号登録
admin.site.register(Material) # 番号登録(材料)
admin.site.register(NameEntry) # 名前とアルファベットの紐付け
admin.site.register(FullReportData) # 損傷写真帳の全データ
# admin.site.register(DamageComment) # 所見データ
admin.site.register(DamageList) # 損傷一覧
""" 管理サイトの並び替え表示に必要な動作 """
class CustomPartsNameFilter(admin.SimpleListFilter):
    title = 'Parts Name'
    parameter_name = 'replace_name'

    def lookups(self, request, model_admin):
        return [
            ('主桁', '主桁'),
            ('横桁', '横桁'),
            ('床版', '床版'),
            ('排水管', '排水管')
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(replace_name__icontains=self.value())
        return queryset

@admin.register(DamageComment)
class DamageCommentAdmin(admin.ModelAdmin):
    list_display = ('span_number', 'parts_name', 'parts_number', 'damage_name', 'number')
    list_filter = (CustomPartsNameFilter,)
    search_fields = ('replace_name__icontains',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            parts_order=Case(
                When(replace_name='主桁', then=0),
                When(replace_name='横桁', then=1),
                When(replace_name='床版', then=2),
                When(replace_name='排水管', then=3),
                default=4,
                output_field=IntegerField(),
            )
        ).order_by('span_number', 'replace_name', 'parts_number', 'number')
                  #   1(径間)          主桁　　　　　　　01　　　　　1(腐食)
""""""