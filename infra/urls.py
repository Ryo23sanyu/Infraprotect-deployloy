from django.urls import path
from .import views
from .views import file_upload, file_upload_success
from .views import photo_list, photo_upload, selected_photos
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index_view, name='index'),
    path('infra/', views.ListInfraView.as_view(), name='list-infra'),
    path('infra/create/', views.CreateInfraView.as_view(), name='create-infra'),
    path('infra/<int:pk>/detail/', views.DetailInfraView.as_view(), name='detail-infra'),
    path('infra/<int:pk>/delete/', views.DeleteInfraView.as_view(), name='delete-infra'),
    path('infra/<int:pk>/update/', views.UpdateInfraView.as_view(), name='update-infra'),
    path('article/', views.ListArticleView.as_view(), name='list-article'),
    path('article/create/', views.CreateArticleView.as_view(), name='create-article'),
    path('article/<int:pk>/detail/', views.DetailArticleView.as_view(), name='detail-article'),
    path('article/<int:pk>/delete/', views.DeleteArticleView.as_view(), name='delete-article'),
    path('article/<int:pk>/update/', views.UpdateArticleView.as_view(), name='update-article'),
    path('upload/', file_upload, name='file_upload'),
    path('upload/success/', file_upload_success, name='file_upload_success'),
    path('photos/', photo_list, name='photo_list'),
    path('photos/upload/', photo_upload, name='photo_upload'),
    path('photos/selected/', selected_photos, name='selected_photos'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)