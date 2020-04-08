# Generated by Django 2.2.1 on 2020-04-08 01:10

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [("core", "0004_auto_20200228_2153")]

    operations = [
        migrations.CreateModel(
            name="UnionTimelineAuthorRelationship",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="timeline",
                        to="core.Contributor",
                    ),
                ),
                (
                    "timeline",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="authors",
                        to="core.UnionTimeline",
                    ),
                ),
            ],
            options={"unique_together": {("timeline", "author")}},
        )
    ]
