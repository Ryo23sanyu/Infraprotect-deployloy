# Generated by Django 4.2.7 on 2024-06-30 23:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("infra", "0022_delete_number"),
    ]

    operations = [
        migrations.CreateModel(
            name="Main_frame",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "主要部材",
                    models.CharField(
                        choices=[("有り", "有り"), ("無し", "無し")], max_length=50
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Material",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "材料",
                    models.CharField(
                        choices=[("鋼", "鋼"), ("コンクリート", "コンクリート"), ("その他", "その他")],
                        max_length=50,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="partsnumber",
            name="main_frame",
            field=models.ManyToManyField(to="infra.main_frame"),
        ),
        migrations.AddField(
            model_name="partsnumber",
            name="material",
            field=models.ManyToManyField(to="infra.material"),
        ),
    ]
