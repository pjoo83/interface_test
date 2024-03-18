from django.http import JsonResponse
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def translate_bar(request):
    legend = ['fuck', 'curry']
    data_list = [
        {
            "name": 'fuck',
            "type": 'bar',
            "data": [1, 20, 36, 10, 10, 90, 1, 20, 36, 10, 10, 90, 1, 20, 36, 10, 10, 90]
        },
        {
            "name": 'curry',
            "type": 'bar',
            "data": [1, 20, 36, 10, 10, 90, 1, 20, 36, 10, 10, 90,1, 20, 36, 10, 10, 90]
        }
    ]
    date_list = ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '一月', '二月', '三月', '四月', '五月', '六月',
                 '七月', '五月', '六月',
                 '七月', '五月', '六月',
                 '七月']

    result = {
        "status": True,
        "data": {
            "legend": legend,
            "data_list": data_list,
            "date_list": date_list
        }
    }
    return JsonResponse(result)
