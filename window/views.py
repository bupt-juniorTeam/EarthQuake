import json

from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse, JsonResponse

from django.http import HttpResponse, FileResponse
from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line
from window.crud import *


def base(request):
    return render(request, 'window/base.html')


def lists(request):
    # if request.method=='POST':
    #     return HttpResponse('asd')
    th = ['来源', '地点', '时间', '经度', '维度']

    objects = get_earthquake(0, 10)
    Rows = list()
    for i in range(10):
        Rows.append([get_source_desc(objects[i].source),
                     get_earthquake_desc(objects[i].where),
                     get_time_desc(str(objects[i].when)),
                     objects[i].latitude])
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
    return render(request, 'window/lists.html',
                  {'th': th, 'rows': rows, 'rows_range': paginator.page_range})


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
    columns = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
    frequency_Mia = [0.00686341, 0.16525505, 0.06423721, 0.02455568, 0.08432669, 0.09781415,
                     0.1819265, 0.03405159, 0.00518489, 0.19687783, 0.03675546, 0.10215155]
    frequency_Kun = [0.06329212, 0.11706359, 0.07749633, 0.01901045, 0.00198184, 0.05137212,
                     0.10303296, 0.16241123, 0.24436542, 0.14581221, 0.00485712, 0.0093046]
    frequency_Kai = [0.14999468, 0.23061133, 0.21486037, 0.03056881, 0.03298941, 0.00217304,
                     0.04333368, 0.0789938, 0.12009764, 0.0481514, 0.02209792, 0.02612792]

    bar = (
        Bar()
            .add_xaxis(["二级", "三级", "四级", "五级", "六级", "七级", "八级"])
            .add_yaxis("四川省", [2, 3, 2, 1, 1, 0, 0])
            .add_yaxis("云南省", [3, 4, 3, 2, 0, 0, 0])
            .add_yaxis("河南省", [4, 1, 2, 1, 0, 0, 0])
            .set_global_opts(
            xaxis_opts=opts.AxisOpts(name="震级"),
            yaxis_opts=opts.AxisOpts(name="发生地震城市数目"),
            title_opts=opts.TitleOpts(title="2009年省份灾情震级图"))
    )

    line = (
        Line()
            .add_xaxis(columns)
            .add_yaxis("绵阳", frequency_Mia)
            .add_yaxis("昆明", frequency_Kun)
            .add_yaxis("开封", frequency_Kai)
            .set_global_opts(
            title_opts=opts.TitleOpts(title="2009年城市发生地震频率图", pos_top="48%"),
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
