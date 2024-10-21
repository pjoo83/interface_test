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
