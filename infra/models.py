from django.db import models

CATEGORY = (('bridge', '橋梁'), ('pedestrian', '歩道橋'), ('other', 'その他'))
LOADGRADE = (('one', '一等橋'),('two', '二等橋'),('three', '三等橋'),('unknown', '不明'))
class Infra(models.Model):
  title = models.CharField(max_length=100)# 橋名
  span_number = models.IntegerField()# 径間数
  length = models.IntegerField()# 橋長
  full_width = models.IntegerField()# 全幅員
  load_name = models.CharField(max_length=50)# 路線名
  latitude = models.CharField(max_length=50)# 緯度
  longitude = models.CharField(max_length=50)# 経度
  code = models.CharField(max_length=50, blank=True)# 橋梁コード
  live_load = models.CharField(max_length=50, blank=True)# 活荷重
  load_grade = models.CharField(max_length=50, blank=True, choices = LOADGRADE)# 等級
  rule_book = models.CharField(max_length=100, blank=True)# 適用示方書
  top_structure = models.CharField(max_length=100)# 上部構造形式
  bottom_structure = models.CharField(max_length=100)# 下部構造形式
  under_structure = models.CharField(max_length=100)# 基礎構造形式
  proximity_method = models.CharField(max_length=100)# 近接方法
  traffic_regulation = models.CharField(max_length=100)# 交通規制
  third_party = models.CharField(max_length=100)# 第三者点検の有無
  coastline_distance = models.CharField(max_length=100)# 海岸線の距離
  road_conditions = models.CharField(max_length=100)# 路下条件
  notices = models.CharField(max_length=100)# 特記事項
  category = models.CharField(max_length=100, choices = CATEGORY)# カテゴリ
  
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