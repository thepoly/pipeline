# Generated by Django 2.0.8 on 2018-10-03 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("lights", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="color", name="B", field=models.IntegerField(default=0)
        ),
        migrations.AlterField(
            model_name="color", name="G", field=models.IntegerField(default=0)
        ),
        migrations.AlterField(
            model_name="color", name="R", field=models.IntegerField(default=255)
        ),
    ]
