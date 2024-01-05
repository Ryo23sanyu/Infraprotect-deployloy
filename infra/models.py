from django.db import models

CATEGORY = (('bridge', '橋梁'), ('pedestrian', '歩道橋'), ('other', 'その他'))
LOADGRADE = (('one', '一等橋'),('two', '二等橋'),('three', '三等橋'),('unknown', '不明'))
class Infra(models.Model):
  title = models.CharField(max_length=100)# 橋名
  径間数 = models.IntegerField()# 径間数
  橋長 = models.IntegerField()# 橋長
  全幅員 = models.IntegerField()# 全幅員
  路線名 = models.CharField(max_length=50)# 路線名
  latitude = models.CharField(max_length=50)# 緯度
  longitude = models.CharField(max_length=50)# 経度
  橋梁コード = models.CharField(max_length=50, blank=True)# 橋梁コード
  活荷重 = models.CharField(max_length=50, blank=True)# 活荷重
  等級 = models.CharField(max_length=50, blank=True, choices = LOADGRADE)# 等級
  適用示方書 = models.CharField(max_length=100, blank=True)# 適用示方書
  上部構造形式 = models.CharField(max_length=100)# 上部構造形式
  下部構造形式 = models.CharField(max_length=100)# 下部構造形式
  基礎構造形式 = models.CharField(max_length=100)# 基礎構造形式
  近接方法 = models.CharField(max_length=100)# 近接方法
  交通規制 = models.CharField(max_length=100)# 交通規制
  第三者点検の有無 = models.CharField(max_length=100)# 第三者点検の有無
  海岸線との距離 = models.CharField(max_length=100)# 海岸線の距離
  路下条件 = models.CharField(max_length=100)# 路下条件
  特記事項 = models.CharField(max_length=100)# 特記事項
  カテゴリー = models.CharField(max_length=100, choices = CATEGORY)# カテゴリー
  
  def __str__(self):
    return self.title
  
CATEGORY = (('bridge', '橋梁'), ('pedestrian', '歩道橋'), ('other', 'その他'))
class Article(models.Model):
  title = models.CharField(max_length=100)# 顧客名
  article_name = models.CharField(max_length=100)# 物件名
  number = models.IntegerField()# 対象数
  manager = models.CharField(max_length=100)# 担当者名
  other = models.CharField(max_length=100)# その他
  category = models.CharField(max_length=100, choices = CATEGORY)# カテゴリ
  
  def __str__(self):
    return self.title
    
class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    
class Photo(models.Model):
    image = models.ImageField(upload_to='photos/')
    
class Company(models.Model):
    name = models.CharField(max_length=100)