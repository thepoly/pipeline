# Generated by Django 5.0.9 on 2024-11-09 03:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_archivespage'),
        ('postline', '0003_rename_extendedarticlepage_postlineindexpage'),
        ('wagtailcore', '0094_alter_page_locale'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostlinePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('posted', models.BooleanField(default=False, help_text='Whether this post has been published to Instagram')),
                ('instagram_link', models.URLField(blank=True, help_text='Link to the Instagram post', null=True)),
                ('article', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='instagram_posts', to='core.articlepage')),
            ],
            options={
                'verbose_name': 'Instagram Post',
                'verbose_name_plural': 'Instagram Posts',
            },
            bases=('wagtailcore.page',),
        ),
    ]