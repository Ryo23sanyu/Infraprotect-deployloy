# アプリ内からインポート
import datetime
# django内からインポート
from django import forms
from django.core.files.storage import default_storage

from .models import CustomUser, Image, Infra, Regulation, UploadedFile
from .models import Photo, Company, Table, NameEntry, PartsNumber

# ファイルアップロード
class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']

# 会社別に表示
class UserCreationForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=Company.objects.all())
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'company']

# << Infra毎にdxfファイルを登録 >>
class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['infra', 'dxf']

# << 各橋作成時のボタン選択肢 >>
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
        
# << 各橋更新時のボタン選択肢 >>
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

# << センサス入力用 >>
class CensusForm(forms.Form):
    traffic = forms.CharField(label='交通量')
    mixing = forms.CharField(label='大型車混入率')
    
# << 名前とアルファベットの紐付け >>
class NameEntryForm(forms.ModelForm):
    class Meta:
        model = NameEntry
        fields = ['name', 'alphabet']

# NameEntryFormSet = modelformset_factory(NameEntry, form=NameEntryForm, extra=3)
#          Formセットを生成するための関数(modelクラス, Formクラス, 最初に表示する空のクラス数)

# << 要素番号の登録 >>
class PartsNumberForm(forms.ModelForm):
    class Meta:
        model = PartsNumber
        # fields = ['parts_name', 'symbol', 'material', 'main_frame', 'number']
        fields = ['parts_name', 'symbol', 'number']
        
# 1回のリクエストで、必ず5個のデータを入力したいときに使う。必ず一定数のデータを入れたいときに使う。
# PartsNumberFormSet = modelformset_factory(PartsNumber, form=PartsNumberForm, extra=5)


# <<損傷写真表示>>
class NameForm(forms.Form):
    initial = forms.CharField(label='イニシャル')
    name = forms.CharField(label='名前')
    folder_path = forms.CharField(label='フォルダパス')
    

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
    
