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
                             'XQiOiJldV9uYyIsInJhdyI6eyJtZXRhIjoiQVdLTmxDL093NEFjWDdVT2l6RUFnQUpsMFoxU1ZvR0FCR1hSblZ' \
                             'KV2dZQUVaclY0N1VIRkFBUUNLZ0VBUVVGQlFVRkJRVUZCUVVKdGRHUnZhM2hLVDBGQmR6MDkiLCJzdW0iOiI5' \
                             'MjcxZTgyZGZhYWRjMGMyYzI0NmM5MWY4ZTQzZjJiMDBiZGQzZjI5YWI5NTdmMzA5MTRiZGNmNDI2MGRhZTk4Ii' \
                             'wibG9jIjoiemhfY24iLCJhcGMiOiJSZWxlYXNlIiwiaWF0IjoxNzM3NTE1OTA0LCJzYWMiOnsiVXNlclN0YWZ' \
                             'mU3RhdHVzIjoiMSIsIlVzZXJUeXBlIjoiNDIifSwibG9kIjpudWxsLCJucyI6ImxhcmsiLCJuc191aWQiOiI3' \
                             'MTAxNDk1MTIwNDg2NDMyNzk2IiwibnNfdGlkIjoiNjg5NjQzNDM5NTM3MzE0MjAxOCIsIm90IjozLCJjdCI6MT' \
                             'cyMzE5Mzg5MywicnQiOjE3Mzc0NzU2MDV9fQ.QWhAOCd-LGdPfjwx0iLNqXq2QxEuwCv2k2r4tiX995QqL281b' \
                             'um4xjndUHLFC3gDx3dFQ4V0F-8GH5K7NXMIRQ; swp_csrf_token=79f10560-3274-46fa-ac6f-797342e' \
                             '6f556; t_beda37=cebb602d4a5402fdbc52cdf0ec3dec5c0b8a677fe2c102a311dd2eaad3eb0174'
        self.feishu_project_url = 'https://project.feishu.cn/open_api/'
        self.qa_list = {7114600958063067138: ["ou_cbfa7c669b9ac8ed1bc6eeba0776188d", '李洁'],
                        7114959719063764995: ["ou_a7030f781da3d86e72cc8509dd5ae8a1", '韩远霖'],
                        7128198138946420739: ["ou_687dacad56496bad19cf82f399502cc7", '崔美娜'],
                        7111559780421943297: ["ou_896dbf409cf36b5ede7a2f03b76c6aa7", '丁双'],
                        7116367759658762242: ["ou_871c93e9629d73362d6535c4f3c31ab8", '宋凯'],
                        7117821729350696961: ["ou_a7229062dd7f9096c36fd7442433357a", '于胜辉'],
                        7078857838898020355: ["ou_acc02ee1849e26dc1cdb30f479ca64a7", '王子钊'],
                        7122034866186633218: ["ou_714c05ee1c5a9a23fd7676824b60506d", "王进国"],
                        7257084699514765315: ["ou_d54069bd861ef54eda3b8366a4253544", '张菁'],
                        7258552016815865884: ["ou_0748fc435d773accf924bb5636f1cbf8", '蒋帅'],
                        7258584511972245505: ["ou_bcfc171ddd4849ab9715cdae977cf830", '李佳'],
                        7117463163087372289: ["ou_6f79454618ce0803c60ebc2030bb0824", '于洋洋'],
                        7201394377279750145: ["ou_11bbc1338deeab2b9dbb4e243ef06b88", '陈奎'],
                        7205168573025697794: ["ou_b70898458f2ae556741f23e11a4f0177", '杨红军'],
                        7212971331053240348: ["ou_4817f7aa7eab5af958755b29d38e8552", '赵孟珠'],
                        7214331666096046081: ["ou_550c5a779745e01141720784be3b56e0", '王卫涛'],
                        7108600627386662914: ["ou_465af79cf82a5b841112f6446ec74937", '汪明'],
                        7114962694473531395: ["ou_ccf3ca3190448e342110d75e265d3ffa", '薛晋琦'],
                        7394541931872747522: ["ou_e87fefd72b49608b687e410263d970e2", '于若宇'],
                        7394917046393241602: ["ou_4a5fd24805b982831f6e3da5fcbc1cb3", '郭一鑫'],
                        7470710967471472659: ["ou_3dcf003a341d678b1f488f23de4c09db", '卢纯斐'],
                        7117512832005980161: ["ou_088d7dc5ebd35650c7820e34b6f38993", '吕昊'],
                        7428387478676996124: ["ou_263cf3031c5dfe98472b0fdedcdb3fd5", '李朝伟'],
                        7117238460611624964: ["ou_baf2770fc108d7429e4fe97f324a9517", '常浩'],
                        7432028714528964612: ["ou_afd46a08ada11e05bdd08c04e04cc354", '王泽宇'],
                        1111111111111111111: ['ou_f8ccb2bf22d0a09df6790c9a59b906fb', '蕾姐'],
                        0: ["0", "暂无"]}
        self.feishu_record_cloud_document = "https://open.feishu.cn/open-apis/bitable/v1/apps/Xl3EbBH6daKFdYsL5Eac6" \
                                            "l8rnDc/tables/tble4vqz6RqVWndL/records"
        self.feishu_record_finished_cloud_document = "https://open.feishu.cn/open-apis/bitable/v1/apps/Xl3EbBH6daKF" \
                                                     "dYsL5Eac6l8rnDc/tables/tblub91U25WmQaaN/records"

        self.feishu_card = ({
            "content": "{\"schema\":\"2.0\",\"config\":{\"update_multi\":true,\"style\":{\"text_size\":{\"normal_v2\":{\"default\":\"normal\",\"pc\":\"normal\",\"mobile\":\"heading\"}}}},\"body\":{\"direction\":\"vertical\",\"padding\":\"12px 12px 12px 12px\",\"elements\":[{\"tag\":\"markdown\",\"content\":\"您有一条新的测试异常数据，请注意查看！！！！！！！\",\"text_align\":\"left\",\"text_size\":\"normal_v2\",\"margin\":\"0px 0px 0px 0px\"},{\"tag\":\"button\",\"text\":{\"tag\":\"plain_text\",\"content\":\"🌞点击查看详情！！！！\"},\"type\":\"default\",\"width\":\"default\",\"size\":\"medium\",\"behaviors\":[{\"type\":\"open_url\",\"default_url\":\"https://rg975ojk5z.feishu.cn/base/Xl3EbBH6daKFdYsL5Eac6l8rnDc?table=tblub91U25WmQaaN&view=vewD2HVVxN\",\"pc_url\":\"\",\"ios_url\":\"\",\"android_url\":\"\"}],\"margin\":\"0px 0px 0px 0px\"}]},\"header\":{\"title\":{\"tag\":\"plain_text\",\"content\":\"异常数据提醒\"},\"subtitle\":{\"tag\":\"plain_text\",\"content\":\"\"},\"template\":\"blue\",\"padding\":\"12px 12px 12px 12px\"}}",
            "msg_type": "interactive",
            "receive_id": ""
        })
        self.feishu_card_url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"