from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import SignupForm
from .models import Company
from django.contrib.auth import get_user_model
from django.views import generic
from django.contrib.auth.mixins import UserPassesTestMixin


class SignupView(CreateView):
  model = User
  form_class = SignupForm
  template_name ='accounts/signup.html'
  success_url = reverse_lazy('index')

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
    model = User
    template_name = 'accounts/my_page.html'
    # モデル名小文字(user)でモデルインスタンスがテンプレートファイルに渡される