from django.apps import AppConfig
from .encode import *
from django.db.models import F
import pandas as pd


class WindowConfig(AppConfig):
    name = 'window'

    def ready(self):
        pass
    # def readEarthQuakeData(self):
    #     earthquake = Earthquake.objects.create(
    #         source=get_source_code('公网'),
    #         where=get_location_code('北京市海淀区'),
    #         when=get_time_code('2021年6月19日15时22分10秒')
    #     )
    #
    #     set = Set.objects.create(
    #         earthquake=earthquake,
    #         set=get_disaster_set_code('人员伤亡及失踪-死亡'),
    #         count=0
    #     )
    #
    #     set.count = F('count') + 1
    #     set.save()
    #     set.refresh_from_db()
    #     affection = Affection.objects.create(
    #         set=set,
    #         index=get_index_code(set.count),
    #         grade=get_grade_code('特大')
    #     )
    #
    #     df= pd.read_excel('filename',sheet_name=0)
    #
    #     df["发震时刻"]="a"
    #     df["震级(M)"]
    #     df["纬度(°)"]
    #     df["经度(°)"]
    #     df["深度(千米)"]
    #     df["参考位置"]