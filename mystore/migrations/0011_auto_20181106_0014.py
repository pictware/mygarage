# Generated by Django 2.1.2 on 2018-11-05 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mystore', '0010_auto_20181105_2228'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['place_path']},
        ),
        migrations.AddField(
            model_name='type',
            name='is_storage',
            field=models.BooleanField(default=False, verbose_name='Is it storage?'),
        ),
    ]
