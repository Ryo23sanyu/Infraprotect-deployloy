from django import forms
from .models import CustomUser, UploadedFile
from .models import Photo, Company, Number

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']
        
class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']
        
# 会社別に表示

class UserCreationForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=Company.objects.all())

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'company')
        
# 番号登録

class NumberForm(forms.ModelForm):
    class Meta:
        model = Number
        fields = '__all__'
        labels = {'name': '名前', 'age': '年齢'}

