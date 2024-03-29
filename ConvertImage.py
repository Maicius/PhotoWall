from PIL import Image
import os
import json
from copy import deepcopy
import util
from tqdm import tqdm
import re

class ConvertImage(object):
    def __init__(self, debug=False):
        # 保存照片信息的json数组
        self.image_json = []
        self.small_url = ''
        self.middle_url = ''
        self.debug = debug

    def read_info(self, config_file="photo_info.txt", debug=False):
        with open(config_file, "r", encoding="utf-8") as r:
            infos = r.readlines()
        info_dict = {}
        if len(infos) == 0:
            print("无额外照片信息，将直接进行照片转换")
            info_dict['title'] = "小麦冬"
            info_dict['sub_title'] = "xiaomaidong.com"
            return info_dict
        else:
            print("发现额外照片信息，将进行解析...")
        info_dict['part'] = []
        img_type = "0"
        for info in infos:
            try:
                # 跳过注释
                info = info.strip()
                if info.startswith("//"):
                    continue
                info_n = info.split("#")
                # 作为标题解析
                if info_n[0] == util.TITLE_KEY:
                    if util.TITLE_KEY in info_dict:
                        util.print_repeat("标题")
                    self.parse_title(info_n, info_dict)

                elif info_n[0] == util.BACK_KEY:
                    if util.BACK_KEY in info_dict:
                        util.print_repeat("背景图片")
                    self.parse_back_img(info_n[1:], info_dict)

                elif info_n[0] == util.DAYS_KEY:
                    if util.DAYS_KEY in info_dict:
                        util.print_repeat("日期")
                    self.parse_days(info_n, info_dict)
                elif info_n[0] == util.MID_KEY:
                    info_dict['page_title'] = info_n[1]
                elif info_n[0].startswith(util.PARTS_KEY):
                    img_type = info_n[0][4:]
                    info_dict['part'].append(dict(part_id=img_type, part_title=info_n[1], part_desc=info_n[2]))

                elif util.check_image_file_name(info_n[0]):
                    info_n = list(map(lambda x: x.strip(), info_n))
                    if info_n[1] == '':
                        info_n[1] = info_n[0].split('.')[0]
                    info_dict[img_type + info_n[0]] = dict(title=info_n[1], desc=info_n[2], type=img_type)
                else:
                    util.print_warning(info)
                    print("注意照片文件名必须带有后缀，支持以下格式的文件：")
                    print("jpg|png|JPG|jpeg|JPEG|PNG|bmp|BMP")

            except BaseException as e:
                if debug:
                    raise e
                util.print_warning(info)
        print("照片信息解析完成")
        return info_dict

    def parse_title(self, title, info_dict):
        """
        解析标题行
        :param title:
        :return:
        """
        try:
            info_dict['title'] = title[1]
            info_dict['sub_title'] = title[2]
        except BaseException:
            util.print_title_warning(title)
            print("程序将使用小麦冬作为默认标题")
            info_dict['title'] = "小麦冬"
            info_dict['sub_title'] = "xiaomaidong.com"

    def parse_days(self, info, info_dict):
        """
        解析日期行
        :param info:
        :param info_dict:
        :return:
        """
        try:
            info_dict['days_back'] = info[1]
            if util.check_date(info[2]):
                info_dict['days'] = info[2]
            else:
                raise RuntimeError
        except BaseException:
            util.print_days_warning(info)

    def parse_back_img(self, info, info_dict):
        """
        解析背景图片行
        :param info:
        :param info_dict:
        :return:
        """
        try:
            info_dict['back'] = info
        except BaseException:
            util.print_back_warning2(info)

    def process_background(self, back_img_list):
        """
        压缩背景图片
        :param back_img_list:
        :return:
        """
        for img in back_img_list:
            try:
                image = Image.open(img)

                shape = (image.height, image.width)
                middle_shape = self.get_middle_shape(shape)
                image.thumbnail(middle_shape)
                image.save(img)
            except FileNotFoundError:
                util.print_back_warning(img)

    def resize_picture(self, image, image_name, image_info_dict, small_path="", middle_path="", small_url="",
                       middle_url="", type=""):
        image_info = {}
        image_key = type + image_name
        shape = (image.height, image.width)
        util.check_file_exist(small_path)
        util.check_file_exist(middle_path)
        small_image = deepcopy(image)
        small_shape = self.get_small_shape(shape)
        # 获取缩略图
        small_image.thumbnail(small_shape, resample=Image.BICUBIC)
        # 保存小图文件
        try:
            small_image.save(os.path.join(small_path, image_name))
        except BaseException as e:
            image_name = image_name + ".png"
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
        if image_key in image_info_dict:
            image_info['name'] = image_info_dict[image_key]['title']
            image_info['desc'] = image_info_dict[image_key]['desc']
        else:
            image_title, image_desc = util.split_image_name(image_name)
            image_info['desc'] = image_desc
            image_info['name'] = image_title

        # 照片的分类
        image_info['type'] = type
        # 唯一区分照片的id，默认文件名，以后用作照片的网页dom的id
        image_info['id'] = type + image_name
        # print(image_name, ' process finish')
        # flex将用于照片对齐
        image_info['flex'] = image_info['small_width'] * 200 / image_info['small_height']
        image_info['show_desc'] = False
        return image_info

    def get_small_shape(self, shape):
        height = shape[0]
        width = shape[1]
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
        height = shape[0]
        width = shape[1]

        if width > height:
            new_width = 1920
            height = new_width * (height / width)
            return (int(new_width), int(height))
        else:
            new_height = 1920
            width = new_height * (width / height)
            return (int(width), int(new_height))

    def copy_info_from_image_dict(self, image_info_dict):
        image_info_json = {}
        image_info_json['title'] = image_info_dict['title']
        image_info_json['sub_title'] = image_info_dict['sub_title']
        image_info_json['back'] = image_info_dict['back']
        image_info_json['part'] = image_info_dict['part']
        if 'days_back' in image_info_dict:
            image_info_json['days_back'] = image_info_dict['days_back']
        if 'days' in image_info_dict:
            image_info_json['days'] = image_info_dict['days']
        image_info_json['page_title'] = image_info_dict['page_title']
        return image_info_json

    def sort_file(self, file_list):
        """
        对文件名进行排序
        :param file_list:
        :return:
        """
        file_list = list(sorted(file_list))
        index = -1
        for i, file in enumerate(file_list):
            digits = re.findall(re.compile('^[0-9]+'), file.strip())
            if not digits:
                break
            else:
                index += 1
        index += 1
        last_file = file_list[index:]
        pre_file = sorted(file_list[:index], key=lambda x: int(re.findall('^[0-9]+', x)[0]))
        pre_file.extend(last_file)
        return pre_file

    def auto_judge_cls(self, path):
        file_list = util.get_file_list(path)
        img_list = []
        dir_list = []
        for file in file_list:
            if util.check_image_file_name(file):
                img_list.append(file)
            if os.path.isdir(os.path.join(path, file)):
                dir_list.append(file)
        return img_list, dir_list

    def do_convert_image(self, path, photo_info="photo_info.txt", new_path=None, request_base_dir=""):
        """
        批量转换照片
        :param path: 原始照片地址
        :param new_path: 转换后的照片地址
        :return:
        """

        # 需要添加的照片信息
        image_info_dict = self.read_info(photo_info, self.debug)
        if new_path == None or len(new_path) == 0:
            new_path = 'image/'

        self.image_json = self.copy_info_from_image_dict(image_info_dict)
        self.image_json['photos'] = []
        # 检查背景图片
        back_img_list = image_info_dict['back']
        # 若用户未提供背景图片，使用默认背景图片
        if len(back_img_list) == 0:
            default_back = list(map(lambda x: os.path.join(request_base_dir, x),
                                    ["/back/back_1.jpg", "/back/back_2.jpg", "/back/back_3.jpg", "/back/back_4.jpg"]))
            self.image_json['back'] = default_back
        if 'days_back' in image_info_dict:
            if len(image_info_dict['days_back']) == 0:
                self.image_json['days_back'] = os.path.join(request_base_dir, "/back/days.jpg")
            else:
                back_img_list.append(image_info_dict['days_back'])

        # 如果new_path 是绝对路径，就将request_base_dir赋值为它
        if len(request_base_dir) == 0 and os.path.isabs(new_path):
            request_base_dir = new_path

        elif len(request_base_dir) > 0 and os.path.isabs(new_path):
            print(util.warning_begin)
            print("当请求路径(request_dir)不为空时，result_dir 不可以为绝对地址")
            print("请将result_dir修改为当前路径下的子文件夹")
            print("请重新输入result_dir路径，按Enter将使用image/作为结果路径")
            new_path = input()
            if new_path.strip() == '':
                new_path = 'image/'
            request_base_dir = os.path.join(request_base_dir, new_path)

        elif len(request_base_dir) != 0 and not util.check_url_ip(request_base_dir) and request_base_dir != new_path:
            print(util.warning_begin)
            print("请求路径(request_dir)似乎不是一个网址或ip")
            print("这种情况下它必须为空或者于结果地址(result_dir)相同")
            request_base_dir = new_path
        elif request_base_dir == new_path:
            pass
        else:

            request_base_dir = os.path.join(request_base_dir, new_path)

        if len(back_img_list) > 0:
            self.process_background(back_img_list)
            print("背景图片压缩完成")

        root_img_list, dir_list = self.auto_judge_cls(path)
        # 有二级目录的情况
        if len(dir_list) > 0:
            try:
                file_list = dir_list
                img_digit_id = 0
                file_list = list(sorted(file_list, reverse=True))
                for files in file_list:
                    old_img_dir = os.path.join(path, files)
                    img_dir = os.path.join(new_path, files)
                    # 转换后的图片保存的位置
                    small_path = os.path.join(img_dir, 'small')
                    middle_path = os.path.join(img_dir, 'middle')
                    temp = os.path.join(request_base_dir, files)
                    small_url = os.path.join(temp, 'small')
                    middle_url = os.path.join(temp, 'middle')
                    type = files
                    img_list = util.get_file_list(old_img_dir)
                    img_list = self.sort_file(img_list)
                    img_list = list(filter(lambda x: util.check_image_file_name(x), img_list))
                    print("\n处理文件夹:" + files + "...")
                    # 进度条
                    pbar = tqdm(total=len(img_list))
                    image_info_list = []
                    for image_name in img_list:
                        img_digit_id += 1
                        image = Image.open(os.path.join(old_img_dir, image_name))
                        try:
                            image_info = self.resize_picture(image, image_name, image_info_dict, small_path, middle_path,
                                                         small_url,
                                                         middle_url, type)

                            print('uniq_id:', img_digit_id)
                            image_info['uniq_id'] = img_digit_id
                            image_info_list.append(image_info)
                        except BaseException as e:
                            if self.debug:
                                raise e
                        pbar.update(1)
                    pbar.close()

                    part_info = list(filter(lambda x: x['part_id'] == files, image_info_dict['part']))
                    if len(part_info) > 0:
                        part_title = part_info[0]['part_title']
                        part_desc = part_info[0]['part_desc']
                    else:
                        part_title = files
                        part_desc = ""

                    self.image_json['photos'].append(
                        dict(part_id=type, part_desc=part_desc, part_title=part_title, photo_info=image_info_list))

            except BaseException as e:
                print("转换照片出错, 请检查填写的文件路径")
                if self.debug:
                    raise e
        # 一级目录的情况
        if len(root_img_list) > 0:
            try:
                print("\n处理根目录...")
                img_list = root_img_list
                type = "root"
                small_path = os.path.join(new_path, 'small')
                middle_path = os.path.join(new_path, 'middle')
                small_url = os.path.join(request_base_dir, 'small')
                middle_url = os.path.join(request_base_dir, 'middle')
                img_list = self.sort_file(img_list)
                img_list = list(filter(lambda x: util.check_image_file_name(x), img_list))
                pbar = tqdm(total=len(img_list))
                image_info_list = []
                for image_name in img_list:
                    image = Image.open(os.path.join(path, image_name))
                    try:
                        image_info = self.resize_picture(image, image_name, image_info_dict, small_path, middle_path,
                                                        small_url,
                                                        middle_url, type)
                        image_info_list.append(image_info)
                    except BaseException as e:
                        if self.debug:
                            raise e
                    pbar.update(1)
                pbar.close()
                part_info = list(filter(lambda x: x['part_id'] == type, image_info_dict['part']))
                if len(part_info) > 0:
                    part_title = part_info[0]['part_title']
                    part_desc = part_info[0]['part_desc']
                elif len(dir_list) > 0:
                    part_title = 'others'
                    part_desc = ''
                else:
                    part_title = ''
                    part_desc = ''
                self.image_json['photos'].append(
                    dict(part_id=type, photo_info=image_info_list, part_title=part_title, part_desc=part_desc))
            except BaseException as e:
                print("\n转换照片出错, 请检查填写的文件路径\n")
                if self.debug:
                    raise e
        image_js = "var image_json = " + json.dumps(self.image_json, ensure_ascii=False) + ";"
        # 结果保存为js文件
        with open('image_json.js', 'w', encoding='utf-8') as w:
            w.write(image_js)


if __name__ == '__main__':
    pass
