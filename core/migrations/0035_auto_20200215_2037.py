# Generated by Django 2.2.9 on 2020-02-15 20:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("core", "0034_remove_office_election_in")]

    operations = [
        migrations.RemoveField(model_name="office", name="description"),
        migrations.AddField(
            model_name="office",
            name="election_in",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                to="core.Election",
            ),
            preserve_default=False,
        ),
    ]
