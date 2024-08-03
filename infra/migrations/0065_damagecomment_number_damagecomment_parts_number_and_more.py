# Generated by Django 4.2.7 on 2024-08-02 14:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("infra", "0064_alter_damagecomment_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="damagecomment",
            name="number",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="damagecomment",
            name="parts_number",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="damagecomment",
            name="replace_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
