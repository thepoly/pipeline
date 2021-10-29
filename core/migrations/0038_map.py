from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0004_archivespage_body')
    ]

    Operations = [
        migrations.CreateModel(
            name='MapPage',
            fields=[
                (
                    'page_ptr',
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.Page",
                    )
                )
            ],
            options={"abstract": False},
            bases=("wagtailcore.page",),
        )
    ]
