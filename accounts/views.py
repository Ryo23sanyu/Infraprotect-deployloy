from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import SignupForm
from infra.models import Company, CustomUser # CustomUserの追加
from django.contrib.auth import get_user_model
from django.views import generic
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm  # ユーザ登録用フォーム
from django.contrib.auth import login, authenticate

class SignupView(CreateView):
    model = CustomUser
    form_class = SignupForm
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        company_name = form.cleaned_data.get('company_name')
        if company_name:
            # get_or_create から filter().first() に変更
            company = Company.objects.filter(name=company_name).first()
            if not company:
                company = Company.objects.create(name=company_name)
            self.object.company = company
            self.object.save()
        return response

    def get_success_url(self):
        return reverse_lazy('accounts:my_page_detail', kwargs={'pk': self.object.pk})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            company_name = form.cleaned_data.get('company_name')
            if company_name:
                # get_or_create から filter().first() に変更
                company = Company.objects.filter(name=company_name).first()
                if not company:
                    company = Company.objects.create(name=company_name)
                user.company = company
            user.save()
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})
  
'''自分しかアクセスできないようにするMixin(My Pageのため)'''
class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = False

    def test_func(self): # 今ログインしてるユーザーのpkと、そのマイページのpkが同じなら許可
        user = self.request.user # ログインしているユーザーを取得
        return user.pk == self.kwargs['pk'] # ログインしているユーザーのpkがURLに含まれるpkと一致するかチェック
        # 一致する場合、Trueを返す


'''マイページ'''
class MyPage(OnlyYouMixin, generic.DetailView):
    model = CustomUser # UserからCustomUserに変更
    template_name = 'accounts/my_page.html'
    # モデル名小文字(user)でモデルインスタンスがテンプレートファイルに渡される

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('accounts:my_page_detail', pk=user.pk) # アプリケーション名を含める
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def my_page_view(request):
    return render(request, 'my_page.html')