from django.urls import path
from .import views
from .views import multi_file_upload, multi_file_upload_success

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
    path('upload/multi/', multi_file_upload, name='multi_file_upload'),
    path('upload/multi/success/', multi_file_upload_success, name='multi_file_upload_success'),
]