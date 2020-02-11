# Generated by Django 2.2.6 on 2019-11-04 10:03

from django.db import migrations, models
import django.db.models.deletion
import djongo.models.fields
import tram.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('assetnummer', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('beschrijving', models.CharField(max_length=70, null=True)),
                ('bevat_logo', models.BooleanField(default=True)),
                ('ip_adres', models.GenericIPAddressField(null=True)),
                ('logo_online', models.BooleanField(default=False)),
                ('telefoonnummer', models.CharField(max_length=10, null=True)),
                ('laatste_storing', models.IntegerField(default=0)),
                ('aantal_omplopen', models.IntegerField(default=0)),
                ('weging', models.IntegerField(default=1)),
                ('laatste_update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Configuratie',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('naam', models.CharField(max_length=50)),
                ('config', djongo.models.fields.ArrayModelField(model_container=tram.models.ConfiguratieElement)),
            ],
        ),
        migrations.CreateModel(
            name='Urgentieniveau',
            fields=[
                ('niveau', models.SmallIntegerField(primary_key=True, serialize=False)),
                ('beschrijving', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LogoData',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('storing', models.IntegerField()),
                ('druk_a1', models.IntegerField()),
                ('druk_a2', models.IntegerField()),
                ('druk_b1', models.IntegerField()),
                ('druk_b2', models.IntegerField()),
                ('kracht_a', models.IntegerField()),
                ('kracht_b', models.IntegerField()),
                ('omloop_a', models.IntegerField()),
                ('omloop_b', models.IntegerField()),
                ('tijdstip', models.DateTimeField(auto_now=True)),
                ('assetnummer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tram.Asset')),
            ],
        ),
        migrations.CreateModel(
            name='ConfiguratieElement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inputnummer', models.SmallIntegerField()),
                ('signaaltype', models.CharField(choices=[('analoog', 'Analoog'), ('pulse', 'Dig. pulse'), ('digitaal', 'Digitaal')], default='digitaal', max_length=15)),
                ('beschrijving', models.CharField(max_length=50, null=True)),
                ('urgentieniveau', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tram.Urgentieniveau')),
            ],
        ),
        migrations.AddField(
            model_name='asset',
            name='configuratie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tram.Configuratie'),
        ),
        migrations.CreateModel(
            name='AbsoluteData',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('storing', djongo.models.fields.ListField()),
                ('druk_a1', models.IntegerField()),
                ('druk_a2', models.IntegerField()),
                ('druk_b1', models.IntegerField()),
                ('druk_b2', models.IntegerField()),
                ('kracht_a', models.IntegerField()),
                ('kracht_b', models.IntegerField()),
                ('omloop_a', models.IntegerField()),
                ('omloop_b', models.IntegerField()),
                ('tijdstip', models.DateTimeField(auto_now=True)),
                ('assetnummer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tram.Asset')),
            ],
        ),
    ]
