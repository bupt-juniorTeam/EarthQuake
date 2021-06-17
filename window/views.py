from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse

from window.crud import *
import os

def base(request):
    return render(request, 'window/base.html')


def lists(request):
    # if request.method=='POST':
    #     return HttpResponse('asd')
    th = ['来源', '地点', '时间', '经度','维度']

    objects = get_earthquake(0,10)
    Rows=list()
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
    return render(request, 'window/report.html')


def report_earthquake(request):
    source = request.POST['source']
    where = request.POST['province'] + request.POST['city'] + request.POST['area']
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


