import unittest
from PIL import Image
import os
from ConvertImage import ConvertImage
import util
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
        self.ci.do_convert_image(image_dir, new_path="resource/", cls=1)

    def test_do_convert_image_cls2(self):
        file_path = "/Users/maicius/Pictures/2018宝宝"
        new_path = "image/"
        ci = ConvertImage(debug=True)
        ci.do_convert_image(file_path, new_path=new_path, cls=2)

if __name__ =='__main__':
    unittest.main()