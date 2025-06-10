class Feishu_data:
    def __init__(self):
        # 获取自建应用
        self.req_token_body = {
            "app_id": "cli_a53891a386b0d00c",
            "app_secret": "3GLTo0F66pbjveu8zfe36dZ0HFBFma64"
        }
        # 自建应用的url
        self.app_access_token_url = 'https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal'

        self.user_access_token = 'https://open.feishu.cn/open-apis/authen/v1/oidc/access_token'
        self.tenant_access_token_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        self.content_type = {"Content-Type": "application/json; charset=utf-8"}
        self.content_type1 = {
            "Content-Type": "application/json;charset=utf-8",
            'Authorization': ""
        }
        # 文件上传
        self.upload_url = 'https://open.feishu.cn/open-apis/drive/v1/files/upload_all'

        # 文件夹固定token
        self.translate_token = "Af0XfcOGYlhq8zdaQoecB9FBn8c"
        # 获取总文件夹清单=========文件夹清单token需要手动获取
        self.year_filelist_url = "https://open.feishu.cn/open-apis/drive/v1/files?direction=DESC&folder_token" \
                                 "=Af0XfcOGYlhq8zdaQoecB9FBn8c&order_by=EditedTime"

        self.month_filelist_url = "https://open.feishu.cn/open-apis/drive/v1/files?direction=DESC&folder_token" \
                                  "=EHQvfnHFOl0yJhdcYHUcZAKDnhA&order_by=EditedTime"

        # 创建文件夹
        self.create_folder_url = 'https://open.feishu.cn/open-apis/drive/v1/files/create_folder'

        # 获取机器人所在的群id
        self.get_chats_id_url = 'https://open.feishu.cn/open-apis/im/v1/chats'

        # 发送信息接口
        self.send_msg_url = 'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id'

        # 上传后的文件通用链接
        self.file_url = 'https://rg975ojk5z.feishu.cn/file/'

        # 表格创建
        self.create_sheets = 'https://open.feishu.cn/open-apis/sheets/v3/spreadsheets'

        self.feishu_cookie = 'is_anonymous_session=; passport_web_did=7336818244927455236; ' \
                             'Hm_lvt_e78c0cb1b97ef970304b53d2097845fd=1712126980; meego_local=28800; ' \
                             'QXV0aHpDb250ZXh0=afeac33ca2c8436b8858ad2d3e2cc623; ' \
                             'passport_trace_id=7383876753138499587; ' \
                             'session=XN0YXJ0-df5j42d6-c913-4362-a377-5b1ba18f4a18-WVuZA; ' \
                             'session_list=XN0YXJ0-df5j42d6-c913-4362-a377-5b1ba18f4a18-WVuZA; ' \
                             '__tea__ug__uid=7385428524696258059; _gcl_au=1.1.684665060.1731563513; lang=zh; ' \
                             'locale=zh; i18n_locale=zh; meego_flow_diversion=1735095032864fd392845; ' \
                             'login_asset_key=Asset_c23c250d-ee23-458a-828a-425c7051ec7a; ' \
                             'login_tenant_key=saas_87bdc41b-b987-41dc-98e4-5b87f046b4bf; is_collaborator=false; ' \
                             'server_language=zh; meego_user_key=7117238460611624964; ' \
                             'meego_tenant_key=saas_87bdc41b-b987-41dc-98e4-5b87f046b4bf; ' \
                             '_uuid_hera_ab_path_1=7457836975496888323; _ga=GA1.2.526735565.1640239490; ' \
                             '_ga_VPYRHN104D=GS1.1.1736492580.123.1.1736493428.58.0.0; ' \
                             '_csrf_token=7ed746fb4e0666e5665a50adcf3078507599584b-1737183122; ' \
                             'second_nav_local_data={%227117238460611624964%22:{%22collaporation%22:{' \
                             '%2262a6fce5ed2541be7bf5c2d3%22:{%22function%22:{' \
                             '%22extraListFolded%22:true%2C%22scopeExpanded%22:true}%2C%22personal%22:{' \
                             '%22expandedKeys%22:[' \
                             '%228031849%22%2C%228031847%22%2C%228031850%22%2C%228031855%22%2C%228031854%22]%2C' \
                             '%22scopeExpanded%22:true}%2C%22share%22:{' \
                             '%22scopeExpanded%22:false}}%2C%2262b43f7052bb47de245eabf4%22:{}}%2C%22favorite%22:{}}}; ' \
                             'passport_app_access_token=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9' \
                             '.eyJleHAiOjE3Mzc1NTcwODUsInVuaXQiOiJldV9uYyIsInJhdyI6eyJtX2FjY2Vzc19pbmZvIjp7IjEwNCI6ey' \
                             'JpYXQiOjE3Mzc1MTM4ODUsImFjY2VzcyI6dHJ1ZX19LCJzdW0iOiI5MjcxZTgyZGZhYWRjMGMyYzI0NmM5MWY4Z' \
                             'TQzZjJiMDBiZGQzZjI5YWI5NTdmMzA5MTRiZGNmNDI2MGRhZTk4In19.XJbupsXi4Y7u6vbzuH6xJew_46nlgau' \
                             'NI79co8koxoWR1DrRllH8OB5CMzP6B8Vob3jek5lRwhPtsDO4DGIvog; sub_nav_width=3; meego_csrf_to' \
                             'ken=1UHWDVlD-wc4r-JbRg-TOdF-yplZbQkTblTb; meego_csrf_token=1UHWDVlD-wc4r-JbRg-TOdF-yplZ' \
                             'bQkTblTb; sl_session=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3Mzc1NTkxMDQsInVua' \
                             'XQiOiJldV9uYyIsInJhdyI6eyJtZXRhIjoiQVdLTmxDL093NEFjWDdVT2l6RUFnQUpsMFoxU1ZvR0FCR1hSblZKV2dZQUVaclY0N1VIRkFBUUNLZ0VBUVVGQlFVRkJRVUZCUVVKdGRHUnZhM2hLVDBGQmR6MDkiLCJzdW0iOiI5MjcxZTgyZGZhYWRjMGMyYzI0NmM5MWY4ZTQzZjJiMDBiZGQzZjI5YWI5NTdmMzA5MTRiZGNmNDI2MGRhZTk4IiwibG9jIjoiemhfY24iLCJhcGMiOiJSZWxlYXNlIiwiaWF0IjoxNzM3NTE1OTA0LCJzYWMiOnsiVXNlclN0YWZmU3RhdHVzIjoiMSIsIlVzZXJUeXBlIjoiNDIifSwibG9kIjpudWxsLCJucyI6ImxhcmsiLCJuc191aWQiOiI3MTAxNDk1MTIwNDg2NDMyNzk2IiwibnNfdGlkIjoiNjg5NjQzNDM5NTM3MzE0MjAxOCIsIm90IjozLCJjdCI6MTcyMzE5Mzg5MywicnQiOjE3Mzc0NzU2MDV9fQ.QWhAOCd-LGdPfjwx0iLNqXq2QxEuwCv2k2r4tiX995QqL281bum4xjndUHLFC3gDx3dFQ4V0F-8GH5K7NXMIRQ; swp_csrf_token=79f10560-3274-46fa-ac6f-797342e6f556; t_beda37=cebb602d4a5402fdbc52cdf0ec3dec5c0b8a677fe2c102a311dd2eaad3eb0174'
        self.feishu_project_url = 'https://project.feishu.cn/open_api/'
