# Generated by Django 2.0.8 on 2018-09-03 18:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("core", "0001_initial"), ("articles", "0002_auto_20180831_1737")]

    operations = [
        migrations.AlterUniqueTogether(
            name="articleauthorrelationship", unique_together={("article", "author")}
        )
    ]