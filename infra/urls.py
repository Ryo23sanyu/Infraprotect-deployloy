from django.urls import path
from .import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('infra/', views.ListInfraView.as_view(), name='list-infra'),
    path('infra/<int:pk>/detail/', views.DetailInfraView.as_view(), name='detail-infra'),
    path('infra/create/', views.CreateInfraView.as_view(), name='create-infra'),
    path('infra/<int:pk>/delete/', views.DeleteInfraView.as_view(), name='delete-infra'),
    path('infra/<int:pk>/update/', views.UpdateInfraView.as_view(), name='update-infra'),
    path('infra/<int:pk>/article/', views.ArticleInfraView.as_view(), name='article-infra'),
]