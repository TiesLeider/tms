# Generated by Django 2.2.7 on 2019-11-29 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tram', '0024_auto_20191126_1418'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssetLaatsteData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assetnummer', models.ForeignKey(on_delete=None, to='tram.Asset')),
                ('laatste_data', models.ForeignKey(on_delete=None, to='tram.AbsoluteData')),
            ],
        ),
    ]
