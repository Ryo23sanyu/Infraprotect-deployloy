from django.db import models
from infra.models import models

class Company(models.Model):
    name = models.CharField(max_length=100)
    
class CustomUser(models.Model):# 追加
    name = models.CharField(max_length=100)