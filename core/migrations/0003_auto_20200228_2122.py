# Generated by Django 2.2.1 on 2020-02-28 21:22

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [("core", "0002_auto_20200228_2120")]

    operations = [
        migrations.AlterField(
            model_name="uniontimeline",
            name="events",
            field=wagtail.core.fields.StreamField(
                [
                    (
                        "event",
                        wagtail.core.blocks.StructBlock(
                            [
                                (
                                    "title",
                                    wagtail.core.blocks.RichTextBlock(
                                        default="", required=True
                                    ),
                                ),
                                (
                                    "date",
                                    wagtail.core.blocks.RichTextBlock(
                                        default="", required=True
                                    ),
                                ),
                                (
                                    "body",
                                    wagtail.core.blocks.ListBlock(
                                        wagtail.core.blocks.StructBlock(
                                            [
                                                (
                                                    "phrase",
                                                    wagtail.core.blocks.TextBlock(),
                                                ),
                                                (
                                                    "definition",
                                                    wagtail.core.blocks.RichTextBlock(
                                                        required=False
                                                    ),
                                                ),
                                            ]
                                        )
                                    ),
                                ),
                                (
                                    "featured_image",
                                    wagtail.images.blocks.ImageChooserBlock(
                                        required=False
                                    ),
                                ),
                            ]
                        ),
                    )
                ]
            ),
        )
    ]
