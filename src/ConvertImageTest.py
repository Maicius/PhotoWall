import unittest
from PIL import Image
import os
from src.ConvertImage import ConvertImage
from src import util
import json
class ConvertImageTest(unittest.TestCase):

    def setUp(self) -> None:
        self.ci = ConvertImage()

    def test_check_image_file_name(self):
        res1 = util.check_image_file_name("1.jpg")
        res2 = util.check_image_file_name("1.jpg1")
        res3 = util.check_image_file_name(".jpg")
        res4 = util.check_image_file_name(".JPG")
        res5 = util.check_image_file_name(".@@@@@@@")
        assert res1 == True
        assert res2 == False
        assert res3 == False
        assert res4 == False
        assert res5 == False

    def test_read_config(self):
        config_file = "photo_info_template1.txt"
        infos = self.ci.read_info(config_file, debug=True)
        assert type(infos) == dict
        print(infos)
        with open("info.json", 'w', encoding="utf-8") as w:
            json.dump(infos, w, ensure_ascii=False)

    def test_resize_image(self):
        image_name = "0.jpg"
        image = Image.open(os.path.join("", "resource/image/" + image_name))
        image_info = {}
        image_info = self.ci.resize_picture(image, image_name, image_info, "small", "middle")
        print(image_info)

    def test_do_convert_image(self):
        image_dir = "resource/image/"
        self.ci.do_convert_image(image_dir, new_path="resource/")

    def test_do_convert_image_cls2(self):
        file_path = "/Users/maicius/照片/photo"
        new_path = "image/"
        ci = ConvertImage(debug=True)
        ci.do_convert_image(file_path, new_path=new_path)

    def test_split_name(self):
        test1 = '1骑行.jpg'
        test2 = '222骑行.png'
        test3 = '222川藏线-骑行.jpg'
        test4 = '川藏线.jpg'
        test5 = '123.jpg'
        test6 = '123test-desc.jpg'

        res1, res11 = util.split_image_name(test1)
        res2, res21 = util.split_image_name(test2)
        res3, res31= util.split_image_name(test3)
        res4, res41 = util.split_image_name(test4)
        res5, res51 = util.split_image_name(test5)
        res6, res61 = util.split_image_name(test6)
        assert res1 == '骑行' and res11 == ''
        assert res2 == '骑行' and res21 == ''
        assert res3 == '川藏线' and res31 == '骑行'
        assert res4 == '川藏线' and res41 == ''
        assert res5 == '123' and res51 == ''
        assert res6 == 'test' and res61 == 'desc'

if __name__ =='__main__':
    unittest.main()