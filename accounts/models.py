from django.db import models
from django.contrib.auth.models import User, AbstractUser

class Company(models.Model):
    name = models.CharField(max_length=100)
    # 会社に関する他のフィールドを定義

class UserCompany(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    # ユーザーと会社の関連付けのためのフィールドを定義

class Property(models.Model):
    name = models.CharField(max_length=100)
    company = models.ManyToManyField(Company)
    # 物件に関する他のフィールドを定義
    
class User(AbstractUser):
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.SET_NULL)  # 会社との関連付け