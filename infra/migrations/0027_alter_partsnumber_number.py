# Generated by Django 4.2.7 on 2024-07-04 12:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("infra", "0026_alter_partsnumber_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="partsnumber",
            name="number",
            field=models.CharField(
                max_length=50,
                validators=[
                    django.core.validators.RegexValidator(
                        regex="(^\\d{4}$)|(^\\d{4}~\\d{4}$)"
                    )
                ],
            ),
        ),
    ]
