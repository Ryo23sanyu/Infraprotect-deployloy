# Generated by Django 4.2.7 on 2024-07-30 04:56

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("infra", "0054_alter_damagelist_classification_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="damagelist",
            old_name="Classification",
            new_name="classification",
        ),
    ]
