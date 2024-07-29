# Generated by Django 4.2.7 on 2024-07-24 09:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("infra", "0040_partsnumber_infra"),
    ]

    operations = [
        migrations.AddField(
            model_name="fullreportdata",
            name="damage_coordinate_x",
            field=models.CharField(default=14, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="fullreportdata",
            name="damage_coordinate_y",
            field=models.CharField(default=14, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="fullreportdata",
            name="picture_coordinate_x",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="fullreportdata",
            name="picture_coordinate_y",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="fullreportdata",
            name="span_number",
            field=models.CharField(default=14, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="fullreportdata",
            name="last_time_picture",
            field=models.ImageField(blank=True, null=True, upload_to="pictures/"),
        ),
        migrations.AlterField(
            model_name="fullreportdata",
            name="picture_coordinate",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="fullreportdata",
            name="picture_number",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="fullreportdata",
            name="this_time_picture",
            field=models.ImageField(blank=True, null=True, upload_to="pictures/"),
        ),
    ]
