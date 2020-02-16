# Generated by Django 2.2.9 on 2020-02-15 18:45

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [("core", "0031_auto_20200215_1843")]

    operations = [
        migrations.CreateModel(
            name="CandidateRelatedArticles",
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
                    "sort_order",
                    models.IntegerField(blank=True, editable=False, null=True),
                ),
                (
                    "article",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="core.ArticlePage",
                    ),
                ),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="related_articles",
                        to="core.CandidatePage",
                    ),
                ),
            ],
            options={"ordering": ["sort_order"], "abstract": False},
        ),
        migrations.DeleteModel(name="CandidateRelatedAuthors"),
    ]