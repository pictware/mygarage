# Generated by Django 2.1.2 on 2018-11-04 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mystore', '0008_auto_20181026_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='text',
            field=models.CharField(blank=True, default='', max_length=1024, verbose_name='Text'),
        ),
    ]
