# Generated by Django 3.0.5 on 2020-05-28 14:58

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tram', '0013_auto_20200420_1203'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='absolutedata',
            options={'get_latest_by': 'tijdstip', 'verbose_name': 'data', 'verbose_name_plural': 'data'},
        ),
        migrations.AlterModelOptions(
            name='asset',
            options={'ordering': ['assetnummer']},
        ),
        migrations.AlterField(
            model_name='asset',
            name='alarm_waarde_druk_a',
            field=models.IntegerField(default=750, help_text="Geef de waarde op die het 'Druklimiet'-alarm triggert voor de A-bak"),
        ),
        migrations.AlterField(
            model_name='asset',
            name='alarm_waarde_druk_b',
            field=models.IntegerField(default=750, help_text="Geef de waarde op die het 'Druklimiet'-alarm triggert voor de B-bak"),
        ),
        migrations.AlterField(
            model_name='asset',
            name='assetnummer',
            field=models.CharField(help_text='Het unieke nummer van deze asset', max_length=10, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='asset',
            name='beschrijving',
            field=models.CharField(help_text='Een korte beschrijving van deze asset', max_length=70, null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='configuratie',
            field=models.ForeignKey(default=3, help_text='Configuratie van de asset', null=True, on_delete=django.db.models.deletion.CASCADE, to='tram.Configuratie'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='druk_a1',
            field=models.IntegerField(blank=True, default=0, help_text='De drukwaarde van de afgelopen polling.'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='druk_a2',
            field=models.IntegerField(blank=True, default=0, help_text='De drukwaarde van de afgelopen polling.'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='druk_b1',
            field=models.IntegerField(blank=True, default=0, help_text='De drukwaarde van de afgelopen polling.'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='druk_b2',
            field=models.IntegerField(blank=True, default=0, help_text='De drukwaarde van de afgelopen polling.'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='ip_adres_logo',
            field=models.GenericIPAddressField(blank=True, help_text='Het IP-adres van de storingslogo', null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='ip_adres_modem',
            field=models.GenericIPAddressField(blank=True, help_text='Het IP-adres van de H&K-modem', null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='kracht_a',
            field=models.IntegerField(blank=True, default=0, help_text='De krachtwaarde van de afgelopen polling.'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='kracht_b',
            field=models.IntegerField(blank=True, default=0, help_text='De krachtwaarde van de afgelopen polling.'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='omloop_a',
            field=models.IntegerField(blank=True, default=0, help_text='Het aantal omlopen van de A-bak van deze asset.'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='omloop_b',
            field=models.IntegerField(blank=True, default=0, help_text='Het aantal omlopen van de B-bak deze asset.'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='pollbaar',
            field=models.BooleanField(default=False, help_text='Is asset gereed om te pollen?'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='storing_beschrijving',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, default=list, help_text='De storing die gemeld is tijdens de afgelopen polling.', null=True, size=None),
        ),
        migrations.AlterField(
            model_name='asset',
            name='weging',
            field=models.IntegerField(default=1, help_text='De zwaarte van deze asset, deze waarde wordt gebruikt voor het berekenen van de prioriteitsscore.'),
        ),
        migrations.AlterField(
            model_name='configuratieelement',
            name='beschrijving',
            field=models.CharField(help_text='Korte beschrijving van het signaal / alarm dat op deze input is aangesloten.', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='configuratieelement',
            name='configuratie',
            field=models.ForeignKey(help_text='De configuratie waar dit alarm bij hoort.', on_delete=django.db.models.deletion.DO_NOTHING, to='tram.Configuratie'),
        ),
        migrations.AlterField(
            model_name='configuratieelement',
            name='inputnummer',
            field=models.SmallIntegerField(help_text='Het inputnummer van de LOGO waar het signaal is aangesloten'),
        ),
        migrations.AlterField(
            model_name='configuratieelement',
            name='timeout',
            field=models.IntegerField(default=24, help_text='De timeout is een tijdsperiode in uren waarbij dit alarm mag voorkomen. Als het alarm het alarm voor het eerst getriggerd wordt, gaat deze periode in. Pas als het alarm nog een keer getriggerd wordt binnen deze periode, wordt de storing weergegeven in de lijst op de homepagina. <br> Zet deze waarde op 0 om altijd het alarm weer te geven.'),
        ),
        migrations.AlterField(
            model_name='configuratieelement',
            name='urgentieniveau',
            field=models.ForeignKey(help_text='De zwaarte van dit alarm, deze waarde wordt gebruikt voor het berekenen van de prioriteitsscore.', on_delete=django.db.models.deletion.CASCADE, to='tram.Urgentieniveau'),
        ),
        migrations.AlterField(
            model_name='urgentieniveau',
            name='niveau',
            field=models.SmallIntegerField(help_text='Hoe hoger het niveau, des te zwaarder alarmen met dit niveau worden gerekend.', primary_key=True, serialize=False),
        ),
    ]
