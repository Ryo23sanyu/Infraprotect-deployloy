# Generated by Django 4.2.7 on 2024-01-05 09:16

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("infra", "0021_rename_length_infra_橋長"),
    ]

    operations = [
        migrations.RenameField(
            model_name="infra",
            old_name="full_width",
            new_name="全幅員",
        ),
        migrations.RenameField(
            model_name="infra",
            old_name="span_number",
            new_name="径間数",
        ),
    ]
