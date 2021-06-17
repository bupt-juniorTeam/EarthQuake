import json

from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse, JsonResponse

from django.http import HttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line
from window.crud import *
from pyecharts.globals import CurrentConfig
import os

default_host = CurrentConfig.ONLINE_HOST
custom_host = "https://cdnjs.cloudflare.com/ajax/libs/echarts/4.8.0/"
CurrentConfig.ONLINE_HOST = custom_host


def base(request):
    return render(request, 'window/base.html')


def lists(request):
    # if request.method=='POST':
    #     return HttpResponse('asd')
    th = ['id', '来源', '地点', '时间', '经度', '纬度']

    objects = get_earthquake()
    Rows = list()
    for i in range(len(objects)):
        Rows.append([objects[i].id,
                     get_source_desc(objects[i].source),
                     get_earthquake_desc(objects[i].where),
                     get_time_desc(str(objects[i].when)),
                     objects[i].latitude,
                     objects[i].longitude, ]
                    )

    paginator = Paginator(Rows, 10)
    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            rows = paginator.page(page)
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            rows = paginator.page(1)
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            rows = paginator.page(paginator.num_pages)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
    else:
        rows = []
    return render(request, 'window/lists.html',
                  {'th': th, 'rows': rows, 'rows_range': paginator.page_range})

def sublists(request):
    if(request.method=='GET'):
        th = ['id', '地震id', '灾情类型']
        id = request.GET.get("id")
        objects=Set.objects.filter(Q(earthquake_id=id))
        Rows = list()
        for i in range(len(objects)):
            Rows.append([objects[i].id,
                         objects[i].count,
                         get_disaster_set_desc(objects[i].set), ]
                        )
        paginator = Paginator(Rows, 10)
        if request.method == "GET":
            # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
            page = request.GET.get('page')
            try:
                rows = paginator.page(page)
            except PageNotAnInteger:
                # 如果请求的页数不是整数, 返回第一页。
                rows = paginator.page(1)
            except EmptyPage:
                # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
                rows = paginator.page(paginator.num_pages)
            except InvalidPage:
                # 如果请求的页数不存在, 重定向页面
                return HttpResponse('找不到页面的内容')
        return render(request, 'window/sublist.html',
                      {'th': th, 'rows': Rows, 'rows_range': paginator.page_range})


def download(request):
    # cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # filename=str(cwd) + '\\' + "data" + ".json"
    # f = open(filename,'w')
    # f.write(Earthquake.objects.all())
    # response = FileResponse(open(filename, "rb"))
    # response['Content-Type'] = "application/octet-stream"
    # response['Content-Disposition'] = 'attachment;filename=abc.jdon'

    data = {}
    province = serializers.serialize("json", Earthquake.objects.all())
    data["data"] = json.loads(province)

    response= FileResponse(json.loads(province))
    response['Content-Type'] = "application/octet-stream"
    response['Content-Disposition'] = 'attachment;filename="data.json"'

    return response

def genByWhenAndWhere(request):
    when = request.GET.get('when')
    where = request.GET.get('where')

    cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    f = open(cwd + '\\' + when + " - " + where + ".txt", 'w')
    f.write(retrieve_earthquake(where, when))
    response = FileResponse(open(cwd + '\\' + when + " - " + where + ".txt", "rb"))
    response['Content-Type'] = "application/octet-stream"
    response['Content-Disposition'] = 'attachment;filename="网站开发说明.md"'
    return response


def report(request):
    if 'city' in request.POST.keys():
        city = request.POST['province']
    if 'area' in request.POST.keys():
        area = request.POST['area']
    location_data = open('window/data/data.json', encoding='utf-8')
    location_dict = json.load(location_data)
    return render(request, 'window/report.html', {'provinces': location_dict.keys})


def report_earthquake(request):
    source = request.POST['source']
    if request.POST['city'] != "市辖区":
        where = request.POST['province'] + request.POST['city'] + request.POST['area']
    else:
        where = request.POST['province'] + request.POST['area']
    when = request.POST['when']
    date, time = when.split('T')
    year, month, day = date.split('-')
    hour, minute, second = time.split(':')
    when = year + month + day + hour + minute + second
    longitude = request.POST['longitude']
    latitude = request.POST['latitude']
    if request.POST['east_or_west'] == 'west':
        longitude = -longitude
    if request.POST['north_or_south'] == 'south':
        latitude = -latitude
    create_new_earthquake(source, where, when, longitude, latitude)
    return redirect('/window/lists/')


@csrf_exempt
def report_affection(request):
    earthquake_id = request.POST['earthquake_id']
    grade = request.POST['disaster_grade']
    set_code = request.POST['disaster_info']
    create_affection(earthquake_id, set_code, grade)
    return redirect('/window/lists/')


def return_data_json(request):
    location_data = open('window/data/data.json', encoding='utf-8')
    location_dict = json.load(location_data)
    return JsonResponse(location_dict)


def graph_vision(request):
    columns = ["1月", "2月", "3月", "4月", "5月", "6月"]
    frequency_Mia = [0.09263889, 0.14027504, 0.45700745, 0.24483201, 0.01616143, 0.04908517]
    frequency_Kun = [0.10187371, 0.21386396, 0.07714241, 0.03004741, 0.29772922, 0.27934329]
    frequency_Kai = [0.03127373, 0.41961386, 0.37733207, 0.01869715, 0.0839328, 0.0691504]

    bar = (
        Bar()
            .add_xaxis(["二级", "三级", "四级", "五级", "六级", "七级", "八级"])
            .add_yaxis("四川省", [2, 3, 2, 1, 1, 0, 0])
            .add_yaxis("云南省", [3, 4, 3, 2, 0, 0, 0])
            .add_yaxis("河南省", [4, 1, 2, 1, 0, 0, 0])
            .set_global_opts(
            xaxis_opts=opts.AxisOpts(name="震级"),
            yaxis_opts=opts.AxisOpts(name="发生地震城市数目"),
            title_opts=opts.TitleOpts(title="2021年省份灾情震级图"))
    )

    line = (
        Line()
            .add_xaxis(columns)
            .add_yaxis("绵阳", frequency_Mia)
            .add_yaxis("昆明", frequency_Kun)
            .add_yaxis("开封", frequency_Kai)
            .set_global_opts(
            title_opts=opts.TitleOpts(title="2021年城市发生地震频率图", pos_top="48%"),
            legend_opts=opts.LegendOpts(pos_top="48%"),
        )
    )

    grid = (
        Grid()
            .add(bar, grid_opts=opts.GridOpts(pos_bottom="60%"))
            .add(line, grid_opts=opts.GridOpts(pos_top="60%"))

    )
    grid.render("window/templates/window/graph.html")
    return render(request, "window/graph.html")


def return_location(request):
    if (request.method == 'GET'):
        location_info = {
            'lat': 34.7,
            'lng': 98.25
        }
        data = json.dumps(location_info)
        return HttpResponse(data)
