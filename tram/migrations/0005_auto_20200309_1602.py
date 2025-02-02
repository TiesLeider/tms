# Generated by Django 2.2.7 on 2020-03-09 16:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tram', '0004_asset_laatste_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='laatste_data',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tram.AbsoluteData'),
        ),
        migrations.AlterField(
            model_name='storing',
            name='laatste_data',
            field=models.ForeignKey(default=None, editable=False, on_delete=django.db.models.deletion.SET_DEFAULT, to='tram.AbsoluteData'),
        ),
    ]
