from django.contrib import admin
from django.db import models
from .models import Approach, DamageComment, DamageList, FullReportData, Infra, Material, PartsName, Table, Article, LoadGrade, LoadWeight, Regulation, Rulebook, Thirdparty, UnderCondition, PartsNumber, NameEntry
from django.contrib.auth.admin import UserAdmin
from django.db.models import Case, When, Value, IntegerField
from django.db.models import Q
from django.db.models.functions import Substr
from django.db.models.functions import Length, Substr

# models.pyのclass名とカッコの中を合わせる
class InfraAdmin(admin.ModelAdmin): # 橋梁
    list_display = ('title', '径間数', '路線名', 'article')
admin.site.register(Infra, InfraAdmin)

admin.site.register(Article) # 案件
admin.site.register(Regulation) # 道路規制
admin.site.register(LoadWeight) # 活荷重
admin.site.register(LoadGrade) # 等級
admin.site.register(Rulebook) # 適用示方書
admin.site.register(Approach) # 近接方法
admin.site.register(Thirdparty) # 第三者点検の有無
admin.site.register(UnderCondition) # 路下条件
admin.site.register(Material) # 番号登録(材料)

class TableAdmin(admin.ModelAdmin): # 損傷写真帳
    list_display = ('infra', 'article', 'dxf')
admin.site.register(Table, TableAdmin)

class FullReportDataAdmin(admin.ModelAdmin): # 損傷写真帳の全データ
    list_display = ('parts_name', 'damage_name', 'span_number', 'infra', 'article')
    search_fields = ('parts_name', 'infra__title', 'article__案件名') # 検索対象：「infraのtitleフィールド」と指定
    def get_search_results(self, request, queryset, search_term):
        # デフォルトの動作
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        # infra__titleのみ完全一致
        exact_match_query = Q(infra__title=search_term)
        # 既存の部分一致と完全一致を組み合わせる
        queryset = queryset.filter(exact_match_query | Q(parts_name__icontains=search_term) | Q(article__案件名__icontains=search_term))
        return queryset, use_distinct
    # def get_ordering_queryset(self, queryset):
    #     # 並べ替えのための指定順リスト
    #     parts_order_list = ['主桁', '横桁', '床版']
    #     damage_order_list = ['①腐食', '②亀裂', '③ゆるみ・脱落']
        
    #     # parts_nameの指定したリスト順
    #     parts_order_case = Case(
    #         *[When(parts_name__icontains=part, then=index) for index, part in enumerate(parts_order_list)]
    #     )

    #     # parts_nameの末尾4桁（逆順）で並べ替えるための文字列を整数に変換
    #     parts_name_substr = Substr('parts_name', Length('parts_name') - 4 + 1, 4)

    #     # damage_nameの指定したリスト順
    #     damage_order_case = Case(
    #         *[When(damage_name__icontains=damage, then=index) for index, damage in enumerate(damage_order_list)]
    #     )

    #     # parts_order_case, parts_name_substr, damage_order_caseの順番で並び替え
    #     queryset = queryset.annotate(
    #         parts_order_val=Case(
    #             *[When(parts_name=part, then=index) for index, part in enumerate(parts_order_list)],
    #             default=len(parts_order_list),
    #             output_field=IntegerField(),
    #         ),
    #         parts_name_end_4_chars=Substr('parts_name', Length('parts_name') - 4 + 1, 4),
    #         damage_order_val=Case(
    #             *[When(damage_name=damage, then=index) for index, damage in enumerate(damage_order_list)],
    #             default=len(damage_order_list),
    #             output_field=IntegerField(),
    #         ),
    #     ).order_by('parts_order_val', 'parts_name_end_4_chars', 'damage_order_val')

    #     return queryset

    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     return self.get_ordering_queryset(qs)
admin.site.register(FullReportData, FullReportDataAdmin)


class DamageListAdmin(admin.ModelAdmin): # 損傷一覧
    list_display = ('parts_name', 'number', 'damage_name', 'damage_lank', 'span_number', 'infra')
    ordering = ('-span_number', '-infra')
admin.site.register(DamageList, DamageListAdmin)


class PartsNameAdmin(admin.ModelAdmin): # 番号登録
    list_display = ('部材名', '記号', 'get_materials', '主要部材', 'display_order') # 表示するフィールド
    list_editable = ('display_order',) # 管理画面でdisplay_orderフィールドを直接編集
    ordering = ('display_order',) # 順序フィールドで並べ替え
    def get_materials(self, obj): # 多対多フィールドの内容をカスタムメソッドで取得して文字列として返す
        return ", ".join([material.材料 for material in obj.material.all()])
    get_materials.short_description = '材料' # 管理画面での表示名を設定
admin.site.register(PartsName, PartsNameAdmin)

class PartsNumberAdmin(admin.ModelAdmin): # 番号登録
    list_display = ('infra', 'parts_name', 'symbol', 'number', 'get_material_list', 'main_frame', 'span_number')
    ordering = ('infra', 'span_number', 'parts_name', 'number')
admin.site.register(PartsNumber, PartsNumberAdmin)

class NameEntryAdmin(admin.ModelAdmin): # 名前とアルファベットの紐付け
    list_display = ('article', 'name', 'alphabet')
admin.site.register(NameEntry, NameEntryAdmin)

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

admin.site.register(DamageComment) # 所見データ
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
""" 管理サイトの並び替え表示に必要な動作（ここまで） """