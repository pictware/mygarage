# Generated by Django 2.0.8 on 2018-10-26 09:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mystore', '0003_auto_20181026_0845'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='root',
            name='high_root',
        ),
        migrations.AlterField(
            model_name='type',
            name='root',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mystore.Type', verbose_name='Root of type'),
        ),
        migrations.DeleteModel(
            name='Root',
        ),
    ]
