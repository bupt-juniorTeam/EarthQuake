# Generated by Django 3.2.3 on 2021-06-17 04:20

from django.db import migrations, models
import pandas as pd
import os
from window.encode import get_source_code, get_location_code, get_time_code
from window.models import Earthquake

def forwards_func(apps, schema_editor):
    # print(os.getcwd())
    df = pd.read_excel('./window/data/eqList.xls')
    for index, row in df.iterrows():
        earthquake = Earthquake.objects.create(
            source=get_source_code('公网'),
            where=get_location_code(row['参考位置']),
            when=get_time_code(row['发震时刻']),
            longitude=row['经度(°)'],
            latitude=row['纬度(°)']
        )
        earthquake.save()

class Migration(migrations.Migration):

    dependencies = [
        ('window', '0002_auto_20210617_0910'),
    ]

    operations = [
        migrations.AddField(
            model_name='earthquake',
            name='latitude',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='earthquake',
            name='longitude',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.RunPython(forwards_func),
    ]


