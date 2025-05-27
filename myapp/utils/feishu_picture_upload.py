import requests
from myapp.utils.feishu_get_token import get_tenant_access_token
from myapp.utils.feishu_data import Feishu_data
import requests
from requests_toolbelt import MultipartEncoder
from PIL import Image, ImageSequence
import subprocess
import pag
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


def convert_pag_to_mp4(pag_path, output_path):
    try:
        pag_file = pag.PAGFile.load("animation.pag")

        # 2. 创建渲染器
        renderer = pag.Renderer()
        renderer.setComposition(pag_file)

        # 3. 设置导出参数
        output_file = "output.mp4"
        width, height = pag_file.width(), pag_file.height()
        fps = 30  # 帧率
        duration = pag_file.duration()  # 获取动画时长

        # 4. 进行渲染并保存
        renderer.renderToFile(output_file, width, height, fps, duration)

        print(f"PAG 文件已成功转换为 {output_file}")
    except subprocess.CalledProcessError as e:
        print("转换失败：")
        print(e.stderr)


# 示例调用

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


def check_png_transparency(file_path):
    """
    :param file_path:
    :return: png头像框透明度检测
    """
    try:
        with Image.open(file_path) as img:
            if img.mode in ("RGBA", "LA"):  # 有 alpha 通道
                alpha = img.getchannel("A")
                # 检查是否存在透明像素（alpha < 255）
                if alpha.getextrema()[0] < 255:
                    return "PNG 图像包含透明通道"
            elif img.info.get("transparency", None) is not None:
                # GIF 图像可能用 transparency index 表示透明
                return "PNG 图像包含透明通道"
        return "PNG 图像背景可能不是透明，请注意！！！！！！！！！"
    except Exception as e:
        return f"False,无法检测透明度: {e}"


def check_webp_animation_alpha(file_path):
    """
    :param file_path:
    :return: web头像框是否包含透明度检测
    """
    try:
        with Image.open(file_path) as img:
            if img.mode == 'RGBA':
                alpha = img.getchannel('A')
                # 检查是否有任何像素 alpha < 255
                return alpha.getextrema()[0] < 255
            elif 'transparency' in img.info:
                return "webp 图像包含透明通道"
            else:
                return "webp 图像背景可能不是透明，请注意！！！！！！！！！"
    except Exception as e:
        print(f"出错: {e}")
        return False



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
    # print(check_image('image.png'))
    # print(check_png_transparency("pendant_file_20250527035139.png"))
    # print(check_png_transparency("pendant_file_20250527064112.png"))

    print(check_webp_animation_alpha('image.webp'))
