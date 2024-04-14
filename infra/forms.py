import datetime
from django import forms
from .models import CustomUser, Image, Number, UploadedFile
from .models import Photo, Company
from django.core.files.storage import default_storage

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

# <<写真表示>>
#class UploadForm(forms.Form):
#    photo = forms.ImageField()
    
# <<損傷写真表示>>
class NameForm(forms.Form):
    initial = forms.CharField(label='イニシャル')
    name = forms.CharField(label='名前')
    folder_path = forms.CharField(label='フォルダパス')
    
# 番号図用(models-forms-viewsの順)
class NumberForm(forms.ModelForm):
    class Meta:
        model   = Number
        fields  = [ "name", "top_number", "bottom_number", "single_number" ]

# 全景写真用
class UploadForm(forms.ModelForm):
    class Meta:
        model = Image  # アップロードする画像を格納するモデル
        fields = ('photo',)  # photoは画像データを格納するフィールド

# 画像変更用(Ajax)
class FileUploadSampleForm(forms.Form):
    file = forms.ImageField()

    def save(self):
        """ファイルを保存するメソッド"""
        now_date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')  # ファイル名に現在時刻を付与するため取得
        upload_file = self.files['file']  # フォームからアップロードファイルを取得
        file_name = default_storage.save(now_date + "_" + upload_file.name, upload_file)  # ファイルを保存 戻り値は実際に保存したファイル名
        return default_storage.url(file_name)