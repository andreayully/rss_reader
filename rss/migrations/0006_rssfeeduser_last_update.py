# Generated by Django 3.1.7 on 2021-03-19 23:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('rss', '0005_feedentries_external_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='rssfeeduser',
            name='last_update',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
