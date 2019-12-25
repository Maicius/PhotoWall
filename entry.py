from src.ConvertImage import ConvertImage
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-image_dir", type=str, default="image/")
parser.add_argument('-result_dir', type=str, default="image/")
parser.add_argument("-request_dir", type=str, default="image/")
parser.add_argument("-photo_info", type=str, default="photo_info.txt")
if __name__ == '__main__':
    """
    批处理程序入口
    """
    args = parser.parse_args()
    print(args.image_dir)
    ci = ConvertImage()
    ci.do_convert_image(path=args.image_dir, new_path=args.result_dir, request_base_dir=args.request_dir,
                        image_info=args.photo_info)
