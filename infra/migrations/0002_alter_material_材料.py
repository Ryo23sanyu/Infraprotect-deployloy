# Generated by Django 4.2.7 on 2024-08-08 10:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("infra", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="material",
            name="材料",
            field=models.CharField(
                choices=[("有り", "有り"), ("無し", "無し")], max_length=100
            ),
        ),
    ]
