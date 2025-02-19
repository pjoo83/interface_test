import requests
from myapp.utils.feishu_get_token import get_tenant_access_token
from myapp.utils.feishu_data import Feishu_data
import requests
from requests_toolbelt import MultipartEncoder

fei = Feishu_data()


# url = "https://gift-resource.starmakerstudios.com/pendant/pendant_webp_file_20250218083245.webp"
# response = requests.get(url)
# with open("image.webp", "wb") as file:
#     file.write(response.content)

def download_img(img_url):
    """
    :param img_url:
    :return:
    """
    url = img_url
    response = requests.get(url)
    if 'png' in url:
        with open("image.png", "wb") as file:
            file.write(response.content)
            return uploadImage('image.png')
    elif 'webp' in url:
        with open("image.webp", "wb") as file:
            file.write(response.content)
            return uploadImage('image.webp')


def uploadImage(img):
    upload_url = "https://open.feishu.cn/open-apis/im/v1/images"
    form = {'image_type': 'message',
            'image': (open(img, 'rb'))}  # 需要替换具体的path
    multi_form = MultipartEncoder(form)
    fei.content_type1['Authorization'] = "Bearer " + f"{get_tenant_access_token()}"
    fei.content_type1['Content-Type'] = multi_form.content_type
    headers = fei.content_type1
    upload_response = requests.request("POST", upload_url, headers=headers, data=multi_form)
    print(upload_response.headers['X-Tt-Logid'])  # for debug or oncall
    print(upload_response.json()['data']['image_key'])  # Print Response
    return upload_response.json()['data']['image_key']


if __name__ == '__main__':
    download_img("https://gift-resource.starmakerstudios.com/pendant/pendant_webp_file_20250218083245.webp")
