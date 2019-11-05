# Generated by Django 2.2.6 on 2019-11-05 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tram', '0003_asset_disconnections'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asset',
            name='laatste_storing',
        ),
        migrations.AddField(
            model_name='asset',
            name='laatste_polling',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='tram.LogoData'),
        ),
    ]
