import requests
from django.utils.safestring import mark_safe
import copy


class Pagination(object):
    def __init__(self, queryset, page_size, plus, page_param="page"):
        query_dict = copy.deepcopy(requests.GET)
        self.query_dict = query_dict
        self.page_param = page_param
        page = request.Get.get(page_param, "1")

        # 是否只包含十进制字符
        if page.isdecimal():
            page = int(page)
        else:
            page = 1

        self.page = page
        self.page_size = page_size
        self.start = (page -1) * page_size
        self.end = page *page_size
        self.page_queryset = queryset[self.start:self.end]

        total_count = queryset.count()
        total_page_count, div =divmod(total_count, page_size)

        if div:
            total_page_count +=1
            self.total_page_count = total_page_count
            self.plus =plus

    def html(self):
        # 计算出当前页面的前五页与后五页
        if self.total_page_count <=2 *self.plus +1:
            # 数据库中的数据条小于11页
            end_page = self.total_page_count
        else:
            # 当前页 >5
            # 当前页+ 5 >总页面
            if(self.page +self.plus) >self.total_page_count:
                start_page = self.total_page_count -2 *self.plus