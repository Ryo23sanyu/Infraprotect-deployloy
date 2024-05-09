from django.db import models
from django.contrib.auth.models import AbstractUser

CATEGORY = (('bridge', '橋梁'), ('pedestrian', '歩道橋'), ('other', 'その他'))
class Article(models.Model):
  案件名 = models.CharField(max_length=100)# 顧客名
  土木事務所 = models.CharField(max_length=100)# 土木事務所 article_name
  対象数 = models.IntegerField()# 対象数 number
  担当者名 = models.CharField(max_length=100)# 担当者名 namager
  その他 = models.CharField(max_length=100)# その他 other
  カテゴリー = models.CharField(max_length=100, choices = CATEGORY)# カテゴリー
  
  def __str__(self):
    return self.案件名


    
CATEGORY = (('bridge', '橋梁'), ('pedestrian', '歩道橋'), ('other', 'その他'))
# LOADGRADE = (('one', '一等橋'),('two', '二等橋'),('three', '三等橋'),('unknown', '不明'))

# 交通規制のモデル
交通規制_CHOICES = (('無し', '無し'),('片側交互通行', '片側交互通行'),('車線減少', '車線減少'),('歩道規制', '歩道規制'),('通行止め', '通行止め'))
class Regulation(models.Model):
    交通規制 = models.CharField(max_length=50, choices=交通規制_CHOICES)
    def __str__(self):
        return self.交通規制
    # returnで戻すため、class内の定義に合わせる
    
活荷重_CHOICES = (('不明', '不明'),('A活荷重', 'A活荷重'),('B活荷重', 'B活荷重'),('TL-20', 'TL-20'),('TL-14', 'TL-14'),('TL-6', 'TL-6'))
class LoadWeight(models.Model):
    活荷重 = models.CharField(max_length=50, choices=活荷重_CHOICES)
    def __str__(self):
        return self.活荷重
    
等級_CHOICES = (('不明', '不明'),('一等橋', '一等橋'),('二等橋', '二等橋'),('三等橋', '三等橋'),('その他', 'その他'))
class LoadGrade(models.Model):
    等級 = models.CharField(max_length=50, choices=等級_CHOICES)
    def __str__(self):
        return self.等級
    
適用示方書_CHOICES = (('不明', '不明'),('平成29年 道路橋示方書', '平成29年 道路橋示方書'),('平成24年 道路橋示方書', '平成24年 道路橋示方書'),('平成14年 道路橋示方書', '平成14年 道路橋示方書'),('平成8年 道路橋示方書', '平成8年 道路橋示方書'),('平成5年 道路橋示方書', '平成5年 道路橋示方書'),('平成2年 道路橋示方書', '平成2年 道路橋示方書'),\
    ('昭和55年 道路橋示方書', '昭和55年 道路橋示方書'),('昭和53年 道路橋示方書', '昭和53年 道路橋示方書'),('昭和47年 道路橋示方書', '昭和47年 道路橋示方書'),('昭和43年 プレストレスコンクリート道路橋示方書', '昭和43年 プレストレスコンクリート道路橋示方書'),\
        ('昭和39年 鉄筋コンクリート道路橋示方書', '昭和39年 鉄筋コンクリート道路橋示方書'),('昭和31年 鋼道路橋設計示方書', '昭和31年 鋼道路橋設計示方書'),('昭和15年 鋼道路橋設計示方書案', '昭和15年 鋼道路橋設計示方書案'),('大正15年 道路構造に関する細則案', '大正15年 道路構造に関する細則案'))
class Rulebook(models.Model):
    適用示方書 = models.CharField(max_length=100, choices=適用示方書_CHOICES)
    def __str__(self):
        return self.適用示方書
    
近接方法_CHOICES = (('地上', '地上'),('梯子', '梯子'),('橋梁点検車', '橋梁点検車'),('高所作業車', '高所作業車'),('軌陸車', '軌陸車'),('ボート', 'ボート'),('ロープアクセス', 'ロープアクセス'),('ドローン', 'ドローン'),('ファイバースコープ', 'ファイバースコープ'),('画像解析', '画像解析'))
class Approach(models.Model):
    近接方法 = models.CharField(max_length=50,choices=近接方法_CHOICES)
    def __str__(self):
        return self.近接方法
    
第三者点検_CHOICES = (('有り', '有り'),('無し', '無し'))
class Thirdparty(models.Model):
    第三者点検 = models.CharField(max_length=50, choices=第三者点検_CHOICES)
    def __str__(self):
        return self.第三者点検

路下条件_CHOICES = (('河川', '河川'),('水路', '水路'),('湖沼', '湖沼'),('海洋', '海洋'),('道路', '道路'),('鉄道', '鉄道'))
class UnderCondition(models.Model):
    路下条件 = models.CharField(max_length=50, choices=路下条件_CHOICES)
    def __str__(self):
        return self.路下条件

class Infra(models.Model):
  title = models.CharField(max_length=100)# 橋名
  径間数 = models.IntegerField()# 径間数
  橋長 = models.DecimalField(max_digits=10, decimal_places=2)# 橋長(最大桁数10桁、小数点以下2桁)
  全幅員 = models.DecimalField(max_digits=10, decimal_places=2)# 全幅員(最大桁数10桁、小数点以下2桁)
  路線名 = models.CharField(max_length=50)# 路線名
  latitude = models.CharField(max_length=50, blank=True)# 緯度
  longitude = models.CharField(max_length=50, blank=True)# 経度
  橋梁コード = models.CharField(max_length=50, blank=True)# 橋梁コード
  活荷重 = models.ManyToManyField(LoadWeight)# 活荷重
  等級 = models.ManyToManyField(LoadGrade)# 等級
  適用示方書 = models.ManyToManyField(Rulebook)# 適用示方書
  上部構造形式 = models.CharField(max_length=100)# 上部構造形式
  下部構造形式 = models.CharField(max_length=100)# 下部構造形式
  基礎構造形式 = models.CharField(max_length=100)# 基礎構造形式
  近接方法 = models.ManyToManyField(Approach)# 近接方法
  交通規制 = models.ManyToManyField(Regulation)# 交通規制
  第三者点検 = models.ManyToManyField(Thirdparty)# 第三者点検の有無
  海岸線との距離 = models.CharField(max_length=100)# 海岸線の距離
  路下条件 = models.ManyToManyField(UnderCondition)# 路下条件
  特記事項 = models.CharField(max_length=100, blank=True)# 特記事項
  カテゴリー = models.CharField(max_length=100, choices = CATEGORY)# カテゴリー
  交通量 = models.CharField(max_length=10, blank=True)# 12時間交通量
  大型車混入率 = models.CharField(max_length=10, blank=True)# 大型車混入率
  article = models.ForeignKey(Article, on_delete=models.CASCADE)
  
  def __str__(self):
    return self.title

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    
# 会社別に表示

class CustomUser(AbstractUser):
    company = models.CharField(max_length=100)

class Company(models.Model):
    name = models.CharField(max_length=100)

# 損傷写真用
# class DamagePicture(models.Model): # DamagePictureという名前のDjangoモデルクラスを定義
#     description = models.CharField(max_length=255, blank=True) # descriptionフィールドを定義
#     document = models.FileField(upload_to='photos/') # documentフィールドを定義、アップロードされたファイルはphotos/に保存される
#     uploaded_at = models.DateTimeField(auto_now_add=True) # uploaded_atフィールドを定義、レコードが作成された日時を自動的に保存
    
# 写真シート
class Panorama(models.Model):
    image = models.ImageField(upload_to='panorama/')
    checked = models.BooleanField(default=False)
    # チェックボックスの状態を保存するフィールド
    # is_checked = models.BooleanField(default=False)

# ファイルアップロード(プライマリーキーで分類分け)
class Uploads(models.Model):
    primary_key = models.AutoField(primary_key=True)
    file = models.FileField(upload_to='uploads/')

class Damage(models.Model):
    notes = models.TextField(blank=True, null=True)
    
# 番号図用(models-forms-viewsの順)
PARTS = (('syuketa', '主桁'), ('yokoketa', '横桁'), ('PCteityakubu', 'PC定着部'))
class Number(models.Model):
    name = models.CharField(max_length=100, choices = PARTS)
    top_number = models.CharField(max_length=5, blank=True)
    bottom_number = models.CharField(max_length=5, blank=True)
    single_number = models.CharField(max_length=5, blank=True)

    def __str__(self):
        return self.name

# 全景写真
class Photo(models.Model):
    image = models.ImageField(upload_to='photos/')

class Image(models.Model):
    #title = models.CharField(max_length=255)  # 画像のタイトル
    photo = models.ImageField(upload_to='photos/')  # 画像ファイル, 'photos/'はMEDIA_ROOT下の保存先ディレクトリ

    #def __str__(self):
    #    return self.photo

# 損傷メモ
class DamageReport(models.Model):
    first = models.CharField(max_length=100)
    second = models.TextField()