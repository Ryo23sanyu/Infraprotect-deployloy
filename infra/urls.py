from django.urls import path
from .import views
from .views import file_upload, file_upload_success
from .views import photo_list, photo_upload, selected_photos, panorama_list
from django.conf import settings
from django.conf.urls.static import static

# urlパスの設定は何を意味しているのか、ぱっと見でわかるように作成する
# 例：article/<int:article_pk>/infra/<int:pk>/update/（article〇番のinfra△番の更新ページ）
urlpatterns = [
    path('', views.index_view, name='index'),
    path('article/<int:article_pk>/infra/', views.ListInfraView.as_view(), name='list-infra'),# 対象橋梁の一覧
    path('article/<int:article_pk>/infra/create/', views.CreateInfraView.as_view(), name='create-infra'),# 橋梁データの登録
    path('article/<int:article_pk>/infra/<int:pk>/detail/', views.DetailInfraView.as_view(), name='detail-infra'),# 橋梁データの一覧
    path('article/<int:article_pk>/infra/<int:pk>/delete/', views.DeleteInfraView.as_view(), name='delete-infra'),# 橋梁データの削除
    path('article/<int:article_pk>/infra/<int:pk>/update/', views.UpdateInfraView.as_view(), name='update-infra'),# 橋梁データの更新
    #                ↑ article の id        ↑ infra の id
    path('article/', views.ListArticleView.as_view(), name='list-article'),# 案件の一覧
    path('article/create/', views.CreateArticleView.as_view(), name='create-article'),# 案件の登録
    path('article/<int:pk>/detail/', views.DetailArticleView.as_view(), name='detail-article'),# 案件のデータ内容
    path('article/<int:pk>/delete/', views.DeleteArticleView.as_view(), name='delete-article'),# 案件の削除
    path('article/<int:pk>/update/', views.UpdateArticleView.as_view(), name='update-article'),# 案件の更新
    
    path('names/', views.names_list_view, name='names-list'),# 名前とアルファベットの紐付け
    
    path('article/<int:article_pk>/infra/<int:pk>/upload/', views.file_upload, name='file-upload'),# ファイルアップロード
    path('article/<int:article_pk>/infra/<int:pk>/output/', views.data_output, name='data-output'),# ファイル出力
    #                ↓ 何のモデルのpkにするか？ ← Tableモデルのid
    #path('article/<int:pk>/infra/bridge_table/', views.bridge_table, name="bridge_table"),# 損傷写真帳
    path('article/<int:article_pk>/infra/<int:pk>/bridge_table/', views.bridge_table, name='bridge_table'),# 損傷写真帳
    
    path('upload/success/', views.file_upload_success, name='file_upload_success'),
    path('photos/', views.photo_list, name='photo_list'),
    path('photos/upload/', views.photo_upload, name='photo_upload'),
    path('photos/selected/', views.selected_photos, name='selected_photos'),
    path('panorama/list/', views.panorama_list, name='panorama_list'),
    path('images/', views.image_list, name='image_list'),# 全景写真
    path('photo/', views.display_photo, name='photo'),# 全景写真のアップロード
    path('change-photo/', views.change_photo, name='change_photo'),# 全景写真の変更
    path('number/', views.number_create_view, name='number'),
    path('opinion/', views.opinion_view, name='opinion'),# 所見一覧
    path('ajax-file-send/', views.ajax_file_send, name='ajax_file_send'),# 損傷写真帳の写真変更
    path('number-entry/', views.number_entry_view, name='number_entry'),# 要素番号登録
    
]
# path('URLの末尾', views.py内の関数名(操作に対するリクエストを受ける), ルーティングに名前を付ける(この名前でURLを参照できるようになる)),
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)