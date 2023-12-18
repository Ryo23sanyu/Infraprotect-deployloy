from django.urls import path
from .views import file_upload, file_upload_success

urlpatterns = [
    path('upload/', file_upload, name='file_upload'),
    path('upload/success/', file_upload_success, name='file_upload_success'),
]