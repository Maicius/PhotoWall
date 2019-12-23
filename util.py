import os
import re
import platform

def read_info(debug=False):
    with open("photo_info.txt", "r", encoding="utf-8") as r:
        infos = r.readlines()
    info_dict = {}
    if len(infos) == 0:
        print("无额外照片信息，将直接进行照片转换")
        return info_dict
    else:
        print("发现额外照片信息，将进行解析...")
    for info in infos:
        try:
            info_n = info.split("#")
            if len(info_n) != 3:
                print_warning(info)
            elif not check_image_file_name(info_n[0]):
                print_warning(info)
                print("照片文件名必须带有后缀，支持以下格式的文件：")
                print("jpg|png|JPG|jpeg|JPEG|PNG|bmp|BMP")
                continue
            info_n = list(map(lambda x: x.strip(), info_n))
            if info_n[1] == '':
                info_n[1] = info_n[0].split('.')[0]
            info_dict[info_n[0]] = dict(title=info_n[1], desc=info_n[2])
        except BaseException as e:
            if debug:
                raise e
            print_warning(info)
    print("照片信息解析完成，共得到" + str(len(info_dict.items())) + "条照片信息")
    return info_dict

def print_warning(info):
    print("警告==================")
    print("警告:照片信息填写格式不符合规范！**可能**会导致照片信息加载出错！")
    print("不规范的文件行：", info)
    print("请严格按照以下格式填写：")
    print("照片文件名#照片标题#照片描述")
    print("示例：0.jpg#小麦冬#详情请戳:www.xiaomaidong.com")

def check_file_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)

def check_image_file_name(name):
    return re.match('.+\.(jpg|png|JPG|jpeg|JPEG|PNG|bmp|BMP)$', name) != None

def get_file_list(path):
    waste_file = '.DS_Store'
    file_list = os.listdir(path)
    # 删除MacOS中带的垃圾文件夹
    if platform.system() == 'Darwin' and waste_file in file_list:
        file_list.remove(waste_file)

    return file_list
