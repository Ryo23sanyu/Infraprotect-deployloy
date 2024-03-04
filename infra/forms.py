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
        labels = {'single_number': '単独番号', 'double_number_one': '連続する始番', 'double_number_two': '連続する末番'}

# <<写真表示>>

class UploadForm(forms.Form):
    photo = forms.ImageField()
    
# <<損傷写真表示>>

class NameForm(forms.Form):
    initial = forms.CharField(label='イニシャル')
    name = forms.CharField(label='名前')
    folder_path = forms.CharField(label='フォルダパス')
