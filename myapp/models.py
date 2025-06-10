from django.db import models
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json

# Create your models here.
'''
用户表
'''
IS_IT_EFFECTIVE3 = (
    ('YES', '是'),
    ('NO', '否'),
)


class interface_user(models.Model):
    name = models.CharField(max_length=500, verbose_name="用户名")
    password = models.CharField(max_length=200, verbose_name="密码")
    mobile = models.CharField(max_length=100, default="", verbose_name="电话号码", null=True, blank=True)
    email = models.EmailField(max_length=200, default="", verbose_name="电子邮件", null=True, blank=True)
    createUser = models.CharField(max_length=200, verbose_name="创建人", null=True, blank=True)
    createTime = models.DateTimeField(max_length=100, auto_now_add=True, null=True, verbose_name="创建时间", blank=True)
    updateTime = models.DateTimeField(auto_now=True, verbose_name="修改时间", null=True, blank=True)
    yn = models.CharField(max_length=100, blank="是否有效", choices=IS_IT_EFFECTIVE3)


# ========================================================================================================================
IS_IT_EFFECTIVE = (
    (1, '是'),
    (2, '否'),
)
'''
业务分类表
'''


class interface_businessCategories(models.Model):
    businessName = models.CharField(max_length=500, verbose_name="业务名称", null=True)
    createUser = models.CharField(max_length=200, verbose_name="创建人")
    updateUser = models.CharField(max_length=200, null=True, verbose_name="修改人")
    createTime = models.DateTimeField(max_length=100, auto_now_add=True, null=True, verbose_name="创建时间", blank=True)
    updateTime = models.DateTimeField(auto_now=True, verbose_name="修改时间", null=True, blank=True)
    yn = models.CharField(max_length=100, verbose_name="是否有效", blank="是否有效", choices=IS_IT_EFFECTIVE, default=1)

    def __str__(self):
        return self.businessName


'''
接口表
'''
IS_IT_EFFECTIVE1 = (
    ('YES', '是'),
    ('NO', '否'),
)
REQUEST_TYPE = (
    ('POST', 'POST'),
    ('GET', 'GET'),
    ('PUT', 'PUT'),
    ('DELETE', 'DELETE')
)
STAUS = (
    ('effective', '有效'),
    ('invalid', '无效'),
)
# noinspection PyRedeclaration
REQUEST_PARAMETER_TYPE_CHOICE = (
    ('form-data', '表单(form-data)'),
    ('raw', '源数据(raw)'),
    ('x-www-form-urlencoded', 'x-www-form-urlencoded')
)


class interface_base(models.Model):
    requestType_choice = (
        (1, "post"),
        (2, "get")
    )
    requestType = models.CharField(max_length=50, verbose_name="请求方式", choices=REQUEST_TYPE)
    businessCategories = models.ManyToManyField(interface_businessCategories, verbose_name="业务分类'")
    interfaceName = models.CharField(max_length=100, verbose_name="接口名称")
    interfaceAddress = models.CharField(max_length=1024, verbose_name="接口地址")
    status = models.CharField(max_length=200, verbose_name="状态", choices=STAUS, null=True, blank=True)
    executeNumber = models.IntegerField(verbose_name="执行次数", null=True, blank=True)
    ownerCase = models.CharField(max_length=200, verbose_name="所属用例", null=True, blank=True)
    yn = models.CharField(max_length=100, blank="是否有效", choices=IS_IT_EFFECTIVE1)
    createUser = models.CharField(max_length=200, verbose_name="创建人")
    updateUser = models.CharField(max_length=200, verbose_name="修改人")
    createTime = models.DateTimeField(max_length=100, auto_now_add=True, null=True, verbose_name="创建时间",
                                      blank=True)
    updateTime = models.DateTimeField(auto_now=True, verbose_name="修改时间", null=True, blank=True)
    requestParameterType = models.CharField(max_length=50, verbose_name='请求参数格式', blank=True, null=True,
                                            choices=REQUEST_PARAMETER_TYPE_CHOICE)

    class Meta:
        ordering = ["-updateTime"]
        verbose_name = '接口'
        verbose_name_plural = '接口管理'

    def __str__(self):
        return self.interfaceName

    @csrf_exempt
    def to_dict(self):
        requestType_dict = {'1': 'post', '2': 'get', '3': 'put', '4': 'delete'}

        return {
            'id': self.id,
            'requestType': requestType_dict[self.requestType],
            'interfaceName': self.interfaceName,
            'interfaceAddress': self.interfaceAddress,
            'status': self.status,
            'updateTime': self.updateTime.strftime("%Y-%m-%d %H:%M:%S"),
            # 'businessCategories': self.businessCategories,
            'executeNumber': self.executeNumber,
            'ownerCase': self.ownerCase,
            'yn': self.yn,
            'createTime': self.createTime.strftime("%Y-%m-%d %H:%M:%S"),
            'createUser': self.createUser,
            'updateUser': self.updateUser,
        }

    # 测试报告详情页点击查看详情需要接口名和地址，views.py报告详情report_test调用的
    def inter_name(self):
        data = {}
        data['interfaceName'] = self.interfaceName
        data['interfaceApi'] = self.interfaceAddress
        return data


class ApiParameter(models.Model):
    api = models.ForeignKey(interface_base, on_delete=models.SET_NULL, null=True, verbose_name="所属接口")
    # ApiHead_name = models.CharField(max_length=1024, verbose_name="head标签")
    # ApiHead_value = models.CharField(max_length=1024, blank=True, null=True, verbose_name='head内容')
    ApiHead = models.CharField(max_length=1024, blank=True, null=True, verbose_name='head内容')
    format = models.CharField(max_length=1024, blank=True, null=True, verbose_name='请求参数格式')
    # name = models.CharField(max_length=1024, verbose_name="参数名")
    # value = models.CharField(max_length=1024, blank=True, null=True, verbose_name='参数值')
    request_value = models.CharField(max_length=1024, blank=True, null=True, verbose_name='参数内容')
    _type = models.CharField(default="String", max_length=1024, verbose_name='参数类型',
                             choices=(('Int', 'Int'), ('String', 'String')))
    required = models.BooleanField(default=True, verbose_name="是否必填")
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name="描述")
    raw_data = models.TextField(blank=True, null=True, verbose_name='raw内容')
    expected_result = models.TextField(blank=True, null=True, verbose_name='预期结果')

    # def __str__(self):
    #     return self.request_value

    @csrf_exempt
    def to_dict(self):
        return {
            'id': self.id,
            'ApiHead': self.ApiHead,
            'request_value': self.request_value,
            '_type': self._type,
            'required': self.required,
            'description': self.description,
            'raw_data': self.raw_data,
            'expected_result': self.expected_result,
            'format': self.format
        }

    def interface_parameter(self):
        req = json.loads(self.request_value)
        request_value = {}
        if req:
            for d in req:
                request_value[d["name"]] = d["value"]
            request_value = json.dumps(request_value)
        else:
            request_value = "无"

        return {
            'request_value': request_value,
            'expected_result': self.expected_result,
        }

    def interface_parameter_raw(self):
        if self.raw_data:
            raw_data = self.raw_data.replace(" ", "")
        else:
            raw_data = "无"
        return {
            'request_value': raw_data,
            'expected_result': self.expected_result,
        }


# 接口测试结果
class interfaceRunResult(models.Model):
    interface_api = models.ForeignKey(interface_base, on_delete=models.CASCADE, verbose_name="所属接口")
    response = models.TextField(verbose_name="响应结果")
    header = models.TextField(verbose_name="响应header")
    statusCode = models.IntegerField(verbose_name="状态码")
    assertResult = models.CharField(max_length=20, null=True, verbose_name="断言结果")


# 接口表测试结果表
class interface_result(models.Model):
    objects = None
    total_interface = models.IntegerField(verbose_name='接口总数', null=False)
    total_pass = models.IntegerField(verbose_name='接口通过数', null=False)
    total_fail = models.IntegerField(verbose_name='接口失败数', null=False)
    total_unexpected = models.IntegerField(verbose_name='未执行的数量', null=True)
    passing_rate = models.FloatField(max_length=15, verbose_name='接口成功率', null=False)
    execution_time = models.FloatField(verbose_name='执行消耗时间时间', null=False)
    responsible_person = models.CharField(max_length=30, verbose_name='接口负责人', default='王子钊', null=True)
    datatime = models.DateTimeField(auto_now_add=True, verbose_name='执行时间', null=True)
    report_url = models.CharField(max_length=300, verbose_name='报告', null=True)


# ui自动化设备表
class channel_ui(models.Model):
    objects = None
    channel_name = models.CharField(max_length=30, verbose_name='客户端名')


# ui自动化
class ui_result(models.Model):
    objects = None
    channel_id = models.ForeignKey(channel_ui, on_delete=models.CASCADE, related_name='books')
    total_case = models.IntegerField(verbose_name='总用例数', null=False)
    total_pass = models.IntegerField(verbose_name='用例通过数', null=False)
    total_fail = models.IntegerField(verbose_name='用例失败数', null=False, default=0)
    total_unexpected = models.IntegerField(verbose_name='未执行的数量', null=True)
    passing_rate = models.FloatField(max_length=15, verbose_name='通过率', null=True)
    live_fail = models.IntegerField(verbose_name='直播模块失败用例数', null=False)
    room_fail = models.IntegerField(verbose_name='语音房模块失败用例数', null=False)
    chat_fail = models.IntegerField(verbose_name='聊天模块失败用例数', null=False)
    me_fail = models.IntegerField(verbose_name='个人模块失败用例数', null=False)
    moment_fail = models.IntegerField(verbose_name='广场模块用例总数', null=False)
    sing_fail = models.IntegerField(verbose_name='唱歌页错误用例数', null=False)
    report_url = models.CharField(max_length=300, verbose_name='报告', null=False)
    datatime = models.DateTimeField(auto_now_add=True, verbose_name='执行时间', null=True)


# 资源变化表
class resource_record(models.Model):
    record_id = models.IntegerField(verbose_name='资源类别', null=False)
    record_number = models.IntegerField(verbose_name='资源现裤中编号', null=False)
    record_name = models.CharField(verbose_name='资源名称', max_length=300, null=True)
    record_png_url = models.CharField(verbose_name='资源头图', max_length=300, null=True)
    record_pag_url = models.CharField(verbose_name='资源视频地址', max_length=300, null=True)
    record_data = models.IntegerField(verbose_name='资源数据', null=True)


# 测试用户表
class test_user(models.Model):
    id = models.IntegerField(max_length=30, verbose_name='顺序Id', primary_key=True)
    user_name = models.CharField(max_length=30, verbose_name='用户名', null=False)
    user_id = models.CharField(max_length=30, verbose_name='用户ID', null=False)


# 测试比记录表
class test_record(models.Model):
    id = models.IntegerField(max_length=30, verbose_name='顺序Id', primary_key=True)
    user_id = models.ForeignKey(test_user, on_delete=models.CASCADE, verbose_name='用户ID')
    record = models.TextField()
