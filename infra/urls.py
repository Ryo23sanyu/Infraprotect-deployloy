from django.urls import path
from .import views
from .views import file_upload, file_upload_success
from .views import photo_list, photo_upload, selected_photos, panorama_list
from django.conf import settings
from django.conf.urls.static import static

# urlパスの設定は何を意味しているのか、ぱっと見でわかるように作成する
# 例：article/<int:article_pk>/infra/<int:pk>/update/（article〇番のinfra△番の更新ページ）
#                   ↑ article の id       ↑ infra の id
urlpatterns = [
    path('', views.index_view, name='index'),
    # << 橋梁関係 >>
    path('article/<int:article_pk>/infra/', views.ListInfraView.as_view(), name='list-infra'),# 対象橋梁の一覧
    path('article/<int:article_pk>/infra/create/', views.CreateInfraView.as_view(), name='create-infra'),# 橋梁データの登録
    path('article/<int:article_pk>/infra/<int:pk>/detail/', views.DetailInfraView.as_view(), name='detail-infra'),# 橋梁データの一覧
    path('article/<int:article_pk>/infra/<int:pk>/delete/', views.DeleteInfraView.as_view(), name='delete-infra'),# 橋梁データの削除
    path('article/<int:article_pk>/infra/<int:pk>/update/', views.UpdateInfraView.as_view(), name='update-infra'),# 橋梁データの更新
    # << 案件関係 >>
    path('article/', views.ListArticleView.as_view(), name='list-article'),# 案件の一覧
    path('article/create/', views.CreateArticleView.as_view(), name='create-article'),# 案件の登録
    path('article/<int:pk>/detail/', views.DetailArticleView.as_view(), name='detail-article'),# 案件のデータ内容
    path('article/<int:pk>/delete/', views.DeleteArticleView.as_view(), name='delete-article'),# 案件の削除
    path('article/<int:pk>/update/', views.UpdateArticleView.as_view(), name='update-article'),# 案件の更新
    # << インプット・アウトプット >>
    path('article/<int:article_pk>/infra/<int:pk>/upload/', views.file_upload, name='file-upload'),# ファイルアップロード
    path('article/<int:article_pk>/infra/<int:pk>/excel_output/', views.excel_output, name='excel-output'),# ファイル出力
    path('article/<int:article_pk>/infra/<int:pk>/dxf_output/', views.dxf_output, name='dxf-output'),# ファイル出力
    # << 損傷写真帳 >>
    path('article/<int:article_pk>/infra/<int:pk>/bridge-table/', views.bridge_table, name='bridge-table'),# 損傷写真帳
    # << 名前の登録 >>
    path('article/<int:article_pk>/names/', views.names_list, name='names-list'),# 名前とアルファベットの紐付け
    # << 要素番号の登録 >>
    path('article/<int:article_pk>/infra/<int:pk>/number/', views.number_list, name='number-list'),# 要素番号登録
    # << 所見一覧 >>
    path('article/<int:article_pk>/infra/<int:pk>/observations/', views.observations_list, name='observations-list'),# 所見一覧
    
    # << 未完成 >>
    path('observations/', views.observer_list, name='observer_list'),# observertionsの形式を見る用(後で消す)
    path('upload/success/', views.file_upload_success, name='file_upload_success'),
    path('photos/', views.photo_list, name='photo_list'),
    path('photos/upload/', views.photo_upload, name='photo_upload'),
    path('photos/selected/', views.selected_photos, name='selected_photos'),
    path('panorama/list/', views.panorama_list, name='panorama_list'),
    path('images/', views.image_list, name='image_list'),# 全景写真
    path('photo/', views.display_photo, name='photo'),# 全景写真のアップロード
    path('change-photo/', views.change_photo, name='change_photo'),# 全景写真の変更
    path('ajax-file-send/', views.ajax_file_send, name='ajax_file_send'),# 損傷写真帳の写真変更
    #path('number/', views.number_create_view, name='number'),
    #path('article/<int:pk>/infra/bridge_table/', views.bridge_table, name="bridge_table"),# 損傷写真帳
    #                   ↑ 何のモデルのpkにするか？ ← Tableモデルのid
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)