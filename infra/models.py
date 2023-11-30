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
  category = models.CharField(max_length=100, choices = CATEGORY)# カテゴリ
  
  def __str__(self):
    return self.title