from django.db.models import F,Q
from django.test import TestCase
from django.urls import resolve
from .models import *
from window.views import lists
from .encode import *
import pandas as pd
import os


class URLTest(TestCase):
    def test_homepage(self):
        found = resolve('/window/')
        print(found.url_name)
        self.assertEqual(found.func, lists)


class ModelTest(TestCase):
    def test_create_affection(self):
        earthquake = Earthquake.objects.create(
            source=get_source_code('公网'),
            where=get_location_code('北京市海淀区'),
            when=get_time_code('2021年6月19日15时22分10秒')
        )
        set = Set.objects.create(
            earthquake=earthquake,
            set=get_disaster_set_code('人员伤亡及失踪-死亡'),
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
        self.assertEqual(Affection.objects.count(), 1)
        affection = Affection.objects.get(id=1)
        self.assertEqual(affection.set.earthquake.source, '101')
        self.assertEqual(affection.set.earthquake.where, '110108000000')
        self.assertEqual(affection.set.earthquake.when, '20210619152210')
        self.assertEqual(affection.set.set, '111')
        self.assertEqual(affection.set.count, 1)
        self.assertEqual(affection.index, '001')
        self.assertEqual(affection.grade, '0')


class DataRead(TestCase):
    def test_read_earthquake(self):
        # print(os.getcwd())
        df= pd.read_excel('./window/data/eqList.xls')
        self.assertTrue(True)

    def test_encode_earthquake(self):
        df = pd.read_excel('./window/data/eqList.xls')
        for index, row in df.iterrows():
            earthquake = Earthquake.objects.create(
                source=get_source_code('公网'),
                where=get_location_code(row['参考位置']),
                when=get_time_code('发震时刻')
            )
            earthquake.save()

    def test_get_earthquake(self):
        return Earthquake.objects.all()

    def test_get_time_desc(self):
        code=	20210524072341
        get_time_desc(str(code))
        a=1+1