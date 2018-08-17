# Generated by Django 2.0.7 on 2018-07-26 19:15

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0020_add-verbose-name'),
        ('articles', '0007_articleauthorrelationship'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepage',
            name='featured_photo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='wagtailimages.Image'),
        ),
        migrations.AlterField(
            model_name='articleauthorrelationship',
            name='article',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.PROTECT, related_name='article_author_relationship', to='articles.ArticlePage'),
        ),
        migrations.AlterField(
            model_name='articleauthorrelationship',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='author_article_relationship', to='authors.AuthorPage'),
        ),
        migrations.AlterField(
            model_name='articlepage',
            name='body',
            field=wagtail.core.fields.StreamField([('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())]),
        ),
    ]