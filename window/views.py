from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
from django.shortcuts import render
from django.http import HttpResponse


def base(request):
    return render(request,'window/base.html')

def lists(request):
    # if request.method=='POST':
    #     return HttpResponse('asd')
    th = ['1', '2', '3', '4']
    Rows = list()
    for i in range(25):
        Rows.append(['1', '2', '3', '4'])
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
    return render(request, 'window/index.html', {'th': th, 'rows': rows})
