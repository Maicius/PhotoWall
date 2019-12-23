from PIL import Image
import numpy as np
import os
import json
from copy import deepcopy
import util

class ConvertImage(object):
    def __init__(self, debug=False):
        """
        :param file_path: 照片所在文件路径，注意这个路径下面的二级目录才是照片文件，一级目录表示照片的分类
        """
        # 保存照片信息的json数组
        self.image_json = []
        # 用于网页加载图片的url地址
        # 这里也可以用相对地址，不加域名
        self.request_base_dir = 'http://www.xiaomaidong.com/fuyuko/images/'
        self.small_url = ''
        self.middle_url = ''
        self.debug = debug

    def resize_picture(self, image, image_name, small_path="", middle_path="", small_url="", middle_url="", type="", image_info_dict=""):
        image_info = {}
        shape = np.shape(image)
        util.check_file_exist(small_path)
        util.check_file_exist(middle_path)
        small_image = deepcopy(image)
        small_shape = self.get_small_shape(shape)
        small_image.thumbnail(small_shape, resample=Image.BICUBIC)
        # 保存小图文件
        small_image.save(os.path.join(small_path, image_name))
        # 保存小图的路径
        image_info['small'] = small_url + '/' + image_name
        # 保存小图的宽和高(加载网页时需要)
        image_info['small_width'] = small_shape[0]
        image_info['small_height'] = small_shape[1]

        middle_shape = self.get_middle_shape(shape)
        image.thumbnail(middle_shape)
        image.save(os.path.join(middle_path, image_name))
        # 保存大图的路径
        image_info['middle'] = middle_url + '/' + image_name
        # 大图的宽和高
        image_info['middle_width'] = middle_shape[0]
        image_info['middle_height'] = middle_shape[1]

        # 照片名称(默认文件名，照片展示时会先显示照片名称和描述)
        image_info['name'] = image_name
        # 照片的描述(手动添加)
        image_info['desc'] = ''

        # 照片的分类(文件夹的分类)
        image_info['type'] = type
        # 唯一区分照片的id，默认文件名，以后用作照片的网页dom的id
        image_info['id'] = image_name
        print(image_name, ' process finish')
        return image_info

    def get_small_shape(self, shape):
        width = shape[1]
        height = shape[0]
        # 针对单反拍的照片，分辨率通常在5000以上
        if width >= 5000:
            return (width // 10, height // 10)

        # 针对航拍的照片
        elif 2000 < width < 5000:
            return (width // 8, height // 8)

        # 针对QQ空间下载的照片
        elif width <= 2000:
            return (width // 3, height // 3)

    def get_middle_shape(self, shape):
        width = shape[1]
        height = shape[0]

        if width > height:
            new_width = 1920
            height = new_width * (height / width)
            return (int(new_width), int(height))
        else:
            new_height = 1920
            width = new_height * (width / height)
            return (int(width), int(new_height))

    def do_convert_image(self, path, new_path=None, cls=1):
        """
        批量转换照片
        :param path: 原始照片地址
        :param new_path: 转换后的照片地址
        :return:
        """
        # 需要添加的照片信息
        image_info_dict = util.read_info(self.debug)
        if new_path == None:
            new_path = path

        # 有二级目录的情况
        if cls == 2:
            try:
                file_list = util.get_file_list(path)
                for files in file_list:
                    img_dir = os.path.join(new_path, files)
                    # 转换后的图片保存的位置
                    small_path = os.path.join(img_dir, 'small')
                    middle_path = os.path.join(img_dir, 'middle')
                    small_url = self.request_base_dir + files + '/small'
                    middle_url = self.request_base_dir + files + '/middle'
                    type = files
                    img_list = util.get_file_list(img_dir)

                    for image_name in img_list:
                        if util.check_image_file_name(image_name):
                            image = Image.open(os.path.join(img_dir, image_name))
                            image_info = self.resize_picture(image, image_name, small_path, middle_path, small_url,
                                                             middle_url, type, image_info_dict)
                            self.image_json.append(image_info)
            except BaseException as e:
                print("转换照片出错, 请检查填写的文件路径")
                print("目前是二级菜单模式，")
                print("即输入路径的路径下面的二级目录才是照片文件，一级目录表示照片的分类")
                print("如需切换到二级目录模式，请重启软件")
                raise e
        # 只有一级目录的情况
        if cls == 1:
            try:
                img_list = util.get_file_list(path)
                small_path = os.path.join(new_path, 'small')
                middle_path = os.path.join(new_path, 'middle')
                small_url = self.request_base_dir + 'small'
                middle_url = self.request_base_dir + 'middle'
                type = ""
                for image_name in img_list:
                    if util.check_image_file_name(image_name):
                        image = Image.open(os.path.join(path, image_name))
                        image_info = self.resize_picture(image, image_name, small_path, middle_path, small_url,
                                                             middle_url, type, image_info_dict)
                        self.image_json.append(image_info)
            except BaseException as e:
                print("转换照片出错, 请检查填写的文件路径")
                print("目前是一级菜单模式，")
                print("即输入路径的路径下就是照片文件，不存在二级目录")
                print("如需切换到二级目录模式，请重启软件")
                raise e

        self.image_json = list(sorted(self.image_json, key=lambda x: x['id']))
        image_js = "var image_json = " + json.dumps(self.image_json)
        # 结果保存为js文件
        with open('image_json.js', 'w', encoding='utf-8') as w:
            w.write(image_js)

if __name__ == '__main__':
    file_path = ""
    new_path = ""
    ci = ConvertImage()
    ci.do_convert_image(file_path, cls=1)
