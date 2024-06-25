# アプリ内からインポート
import datetime
# django内からインポート
from django import forms
from django.core.files.storage import default_storage

from .models import CustomUser, Image, Infra, Number, Regulation, UploadedFile
from .models import Photo, Company, Table

# <<ファイルアップロード>>
class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']

# 会社別に表示
class UserCreationForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=Company.objects.all())

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'company')

# Infra毎にdxfファイルを登録
class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['infra', 'dxf']

# <<各橋作成時のボタン選択肢>>
class BridgeCreateForm(forms.ModelForm):
    class Meta:
        model = Infra
        fields = ['交通規制', '活荷重', '等級', '適用示方書', '近接方法', '第三者点検', '路下条件'] # 他のフィールドについても必要に応じて追加してください。
        widgets = {
            '交通規制': forms.CheckboxSelectMultiple,
            '活荷重': forms.RadioSelect,
            '等級': forms.RadioSelect,
            '適用示方書': forms.RadioSelect,
            '近接方法': forms.CheckboxSelectMultiple,
            '第三者点検': forms.RadioSelect,
            '路下条件': forms.CheckboxSelectMultiple,
        }
        
class BridgeUpdateForm(forms.ModelForm):
    class Meta:
        model = Infra
        fields = ['交通規制', '活荷重', '等級', '適用示方書', '近接方法', '第三者点検', '路下条件'] # 他のフィールドについても必要に応じて追加してください。
        widgets = {
            '交通規制': forms.CheckboxSelectMultiple,
            '活荷重': forms.RadioSelect,
            '等級': forms.RadioSelect,
            '適用示方書': forms.RadioSelect,
            '近接方法': forms.CheckboxSelectMultiple,
            '第三者点検': forms.RadioSelect,
            '路下条件': forms.CheckboxSelectMultiple,
        }

# <<センサス調査>>
class CensusForm(forms.Form):
    traffic = forms.CharField(label='交通量')
    mixing = forms.CharField(label='大型車混入率')
    
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
class UploadForm(forms.ModelForm): # UploadFormという名前のFormクラスを定義(Modelクラスと紐付け)
    photo = forms.ImageField() # modelに定義されているものを使用
    class Meta: # ModelFormと紐付ける場合に記載
        model = Image # models.pyのImageクラスと紐付け
        fields = ['photo'] # Image.modelのphotoフィールドのみを使用

class PhotoUploadForm(forms.ModelForm): # PhotoUploadFormという名前のFormクラスを定義(Modelクラスと紐付け)
    class Meta: # ModelFormと紐付ける場合に記載
        model = Photo # models.pyのPhotoクラスと紐付け
        fields = ['image'] # このFormで扱うフィールドを指定        

# 損傷写真変更用(Ajax)
class FileUploadSampleForm(forms.Form):
    file = forms.ImageField()

    def save(self):
        """ファイルを保存するメソッド"""
        now_date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')  # ファイル名に現在時刻を付与するため取得
        upload_file = self.files['file']  # フォームからアップロードファイルを取得
        file_name = default_storage.save(now_date + "_" + upload_file.name, upload_file)  # ファイルを保存 戻り値は実際に保存したファイル名
        return default_storage.url(file_name)