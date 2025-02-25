import requests
from myapp.utils.feishu_get_token import get_tenant_access_token
from myapp.utils.feishu_data import Feishu_data
import requests
from requests_toolbelt import MultipartEncoder
from PIL import Image

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


def check_png_with_pillow(img):
    """
    :return: 检查png文件是否损坏
    """
    try:
        with Image.open(img) as img:
            img.verify()  # 只验证文件是否损坏，不加载到内存
        return "文件正常未损坏"

    except Exception as e:
        return f"文件损坏: {e}"


def check_png_header(file_path):
    """
    :param file_path:
    :return: 检查png的文件头部
    """
    try:
        with open(file_path, "rb") as f:
            header = f.read(8)
            if header == b'\x89PNG\r\n\x1a\n':
                return f" 文件头部正常"
            else:
                return "PNG 文件头部异常，可能已损坏"
    except Exception as e:
        return f"无法读取文件: {e}"


def check_png_fully_load(file_path):
    """
    :param file_path:
    :return: 检查文件解码
    """
    try:
        with Image.open(file_path) as img:
            img.load()  # 尝试完全加载文件
        return "文件可以完全解码"
    except Exception as e:
        return f"文件解码失败: {e}"


def check_webp_header(file_path):
    """
    :param file_path:
    :return: 检查webp的文件头部
    """
    try:
        with open(file_path, "rb") as f:
            header = f.read(12)
            if header[:4] == b'RIFF' and header[8:] == b'WEBP':
                return " 文件头部正常"
            else:
                return "WebP 文件头异常，可能已损坏"
    except Exception as e:
        return f"无法读取  文件: {e}"


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


def check_image(img):
    """
    :param img: 文件地址
    :return: 返回png三个检查结果
    """
    pillow = check_png_with_pillow(img)
    header = check_png_header(img)
    load = check_png_fully_load(img)
    return pillow, header, load


def check_webp(img):
    """
    :param img: 文件地址
    :return: 返回三个webp检查结果
    """
    pillow = check_png_with_pillow(img)
    header = check_webp_header(img)
    load = check_png_fully_load(img)
    return pillow, header, load

if __name__ == '__main__':
    # download_img("https://gift-resource.starmakerstudios.com/pendant/pendant_webp_file_20250218083245.webp")
    print(check_image('image.png'))
    print(check_webp("image.webp"))
