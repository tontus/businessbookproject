# Generated by Django 3.0.5 on 2020-06-09 03:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_auto_20200609_0335'),
    ]

    operations = [
        migrations.AddField(
            model_name='withdraw_requests',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 6, 9, 3, 36, 47, 124967)),
        ),
        migrations.AlterField(
            model_name='adpack_update',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 6, 9, 3, 36, 47, 118054)),
        ),
        migrations.AlterField(
            model_name='bought_adpack',
            name='buying_date',
            field=models.DateField(default=datetime.datetime(2020, 6, 9, 3, 36, 47, 116390)),
        ),
    ]
