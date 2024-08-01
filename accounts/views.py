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
    model = CustomUser # UserからCustomUserに変更
    form_class = SignupForm
    template_name ='accounts/signup.html'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        #self.object.company = Company.objects.create(name=self.request.POST.get('company_name'))
        company = Company.objects.create(name=self.request.POST.get('company_name'))
        self.object.company = company.name
        self.object.save()
        return response

    def get_success_url(self):
        return reverse_lazy('accounts:my_page_detail', kwargs={'pk': self.object.pk})
    
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # Userオブジェクトを一時保存
            company_name = request.POST.get('company_name') # 入力された会社名を取得
            company = Company.objects.create(name=company_name) # 会社モデルのインスタンスを作成
            user.save() # UserオブジェクトをDBに保存
            user.company = company # ユーザーと会社の関連付け
            user.save() # 会社の関連付けを反映
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})
  
'''自分しかアクセスできないようにするMixin(My Pageのため)'''
class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        # 今ログインしてるユーザーのpkと、そのマイページのpkが同じなら許可
        user = self.request.user
        return user.pk == self.kwargs['pk']


'''マイページ'''
class MyPage(OnlyYouMixin, generic.DetailView):
    model = CustomUser# UserからCustomUserに変更
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