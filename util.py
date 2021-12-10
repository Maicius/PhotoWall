import os
import re
import platform

warning_begin = "警告=================="
TITLE_KEY = "TITLE"
BACK_KEY = "BACK"
DAYS_KEY = "DAYS"
PARTS_KEY = "PART"
MID_KEY = "MID"
def print_warning(info):
    print(warning_begin)
    print("警告:照片信息填写格式不符合规范！**可能**会导致照片信息加载出错！")
    print("不规范的文件行：", info)
    print("请严格按照配置文件填写：")

def print_back_warning(info):
    print(warning_begin)
    print("警告：未发现背景图片，请检查背景图片路径")
    print("路径地址：", info)

def print_title_warning(info):
    print(warning_begin)
    print("照片信息文件的标题行填写格式不正确")
    print(info)
    print("请严格按照一下格式填写：")
    print("title#网页标题#副标题")
    print("title#小麦冬#详情请戳:www.xiaomaidong.com")

def print_back_warning2(info):
    print(warning_begin)
    print("照片信息文件的背景图片行填写格式不正确")
    print(info)

def print_repeat(type):
    print(warning_begin)
    print(type + "行存在重复，请仔细检查配置文件")
    print("程序继续执行，将会覆盖旧" + type)

def print_days_warning(info):
    print(warning_begin)
    print("照片信息文件的日期行填写不正确")
    print(info)
    print("请严格按照以下格式填写：")
    print("DAYS#照片文件名#日期（用/作分割）")
    print("DAYS#back.png#2015/11/09")

def check_date(date):
    return re.match('^[0-9]{4}/[0-9]{2}/[0-9]{2}$', date) != None

def check_file_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)

def check_image_file_name(name):
    return re.match('.+\.(jpg|png|JPG|jpeg|JPEG|PNG|bmp|BMP|HEIC)$', name) != None

def get_file_list(path):
    waste_file = '.DS_Store'
    file_list = os.listdir(path)
    reserve_file = ['middle', 'small']
    # 删除MacOS中带的垃圾文件夹
    if platform.system() == 'Darwin' and waste_file in file_list:
        file_list.remove(waste_file)
    for file in reserve_file:
        if file in file_list:
            file_list.remove(file)
    return file_list

def split_image_name(name):
    """
    传入照片名称，返回照片标题和描述
    :param name:
    :return:
    """
    name = name.split('.')[0]
    image_name_list = name.split('-')
    image_name = re.sub('^[0-9]+(?=[a-zA-Z\u4E00-\u9FA5]+)', '', image_name_list[0])
    if len(image_name_list) > 1:
        image_desc = image_name_list[1]
    else:
        image_desc = ''
    return image_name, image_desc

def check_url_ip(url):
    res = re.findall('\.', url)
    return len(res) > 0

