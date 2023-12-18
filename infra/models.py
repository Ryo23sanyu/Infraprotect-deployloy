from django.db import models

CATEGORY = (('bridge', '橋梁'), ('pedestrian', '歩道橋'), ('other', 'その他'))
class Infra(models.Model):
  title = models.CharField(max_length=100)# 橋名
  span_number = models.IntegerField()# 径間数
  length = models.IntegerField()# 橋長
  full_width = models.IntegerField()# 全幅員
  load_name = models.CharField(max_length=50)# 路線名
  latitude = models.CharField(max_length=50)# 緯度
  longitude = models.CharField(max_length=50)# 経度
  code = models.CharField(max_length=50)# 橋梁コード
  top_structure= models.CharField(max_length=100)# 上部構造形式
  bottom_structure= models.CharField(max_length=100)# 下部構造形式
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
    files = models.FileField(upload_to='uploads/', blank=True, null=True, verbose_name='Files', max_length=255)

class MultiUploadedFile(models.Model):
    files = models.ManyToManyField(UploadedFile)