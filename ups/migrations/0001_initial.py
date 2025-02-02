# Generated by Django 2.2.7 on 2020-03-06 11:06

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assetnummer', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Configuratie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naam', models.CharField(max_length=50)),
                ('config', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='ConfiguratieElement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inputnummer', models.IntegerField()),
                ('beschrijving', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Storing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beschrijving', models.CharField(max_length=100)),
                ('tijdstip', models.DateTimeField(auto_now=True)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pomp.Asset')),
            ],
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('storing', models.IntegerField()),
                ('niveau', models.IntegerField()),
                ('tijdstip', models.DateTimeField(auto_now_add=True)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pomp.Asset')),
            ],
            options={
                'verbose_name_plural': 'Data',
            },
        ),
        migrations.AddField(
            model_name='asset',
            name='configuratie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pomp.Configuratie'),
        ),
    ]
