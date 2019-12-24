import unittest
from PIL import Image
import os
from ConvertImage import ConvertImage
import util
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
        infos = self.ci.read_info()
        assert type(infos) == dict
        print(infos)

    def test_resize_image(self):
        image_name = "0.jpg"
        image = Image.open(os.path.join("", "resource/image/" + image_name))
        image_info = self.ci.resize_picture(image, image_name, "small", "middle")
        print(image_info)

    def test_do_convert_image(self):
        image_dir = "resource/image/"
        self.ci.do_convert_image(image_dir, new_path="resource")

if __name__ =='__main__':
    unittest.main()