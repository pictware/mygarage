# Generated by Django 2.0.8 on 2018-10-26 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mystore', '0002_auto_20181025_2113'),
    ]

    operations = [
        migrations.AddField(
            model_name='type',
            name='prefix_suffix_separator',
            field=models.CharField(blank=True, default='-', max_length=64, verbose_name='Separator for number for this type'),
        ),
        migrations.AlterField(
            model_name='item',
            name='number_suffix',
            field=models.CharField(blank=True, default='', max_length=64, verbose_name='Suffix of number'),
        ),
        migrations.AlterField(
            model_name='root',
            name='number_type',
            field=models.CharField(blank=True, default='', max_length=64, verbose_name='Root part of number'),
        ),
        migrations.AlterField(
            model_name='type',
            name='number_type',
            field=models.CharField(blank=True, default='', max_length=64, verbose_name='Type part of number'),
        ),
    ]
