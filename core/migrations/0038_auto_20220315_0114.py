# Generated by Django 2.2.10 on 2022-03-15 01:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0037_auto_20200326_1525'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contributor',
            options={'ordering': ['name']},
        ),
    ]