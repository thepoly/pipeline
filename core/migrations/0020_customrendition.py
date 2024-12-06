# Generated by Django 5.0.9 on 2024-10-12 05:24

import django.db.models.deletion
import wagtail.images.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_position_term'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomRendition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filter_spec', models.CharField(db_index=True, max_length=255)),
                ('file', wagtail.images.models.WagtailImageField(height_field='height', storage=wagtail.images.models.get_rendition_storage, upload_to=wagtail.images.models.get_rendition_upload_to, width_field='width')),
                ('width', models.IntegerField(editable=False)),
                ('height', models.IntegerField(editable=False)),
                ('focal_point_key', models.CharField(blank=True, default='', editable=False, max_length=16)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='renditions', to='core.customimage')),
            ],
            options={
                'unique_together': {('image', 'filter_spec', 'focal_point_key')},
            },
            bases=(wagtail.images.models.ImageFileMixin, models.Model),
        ),
    ]