# Generated by Django 2.2.7 on 2020-07-30 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tram', '0020_asset_omloop_c'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asset',
            name='omloop_c',
        ),
    ]
