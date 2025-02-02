# Generated by Django 2.2.7 on 2020-03-25 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tram', '0010_auto_20200325_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='laatste_data',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tram.AbsoluteData'),
        ),
        migrations.AlterField(
            model_name='storing',
            name='laatste_data',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to='tram.AbsoluteData'),
        ),
    ]
