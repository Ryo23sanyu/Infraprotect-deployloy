# Generated by Django 4.2.7 on 2024-08-03 02:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("infra", "0065_damagecomment_number_damagecomment_parts_number_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="damagecomment",
            name="comment_parts_name",
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="damagecomment",
            name="replace_name",
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
