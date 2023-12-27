from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import SignupView
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('my_page/<int:pk>/', views.MyPage.as_view(), name='my_page'),
]
