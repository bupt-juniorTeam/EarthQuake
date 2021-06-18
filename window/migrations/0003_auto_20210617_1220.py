# Generated by Django 3.2.3 on 2021-06-17 04:20

from django.db import migrations, models
import pandas as pd
import os

from django.db.models import F

from window.encode import get_source_code, get_location_code, get_time_code, get_disaster_set_code, get_index_code, \
    get_grade_code
from window.models import Earthquake, Set, Affection


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
        set = Set.objects.create(
            earthquake=earthquake,
            set=get_disaster_set_code('人员伤亡及失踪-死亡'),
            count=0
        )
        set.count = F('count') + 1
        set.save()
        set = Set.objects.create(
            earthquake=earthquake,
            set=get_disaster_set_code('人员伤亡及失踪-受伤'),
            count=0
        )
        set.count = F('count') + 1
        set.save()
        set = Set.objects.create(
            earthquake=earthquake,
            set=get_disaster_set_code('人员伤亡及失踪-失踪'),
            count=0
        )
        set.count = F('count') + 1
        set.save()
        set.refresh_from_db()
        affection = Affection.objects.create(
            set=set,
            index=get_index_code(set.count),
            grade=get_grade_code('特大')
        )

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

