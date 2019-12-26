from ConvertImage import ConvertImage
import argparse
from time import sleep
parser = argparse.ArgumentParser()
parser.add_argument("-image_dir", type=str, default="image/")
parser.add_argument('-result_dir', type=str, default="image/")
parser.add_argument("-request_dir", type=str, default="")
parser.add_argument("-photo_info", type=str, default="photo_info.txt")

if __name__ == '__main__':
    """
    批处理程序入口
    """
    args = parser.parse_args()
    print("***************** 照片墙一键生成器*********************")
    print("*******************制作：小麦冬***********************")
    print("原始照片地址：", args.image_dir)
    print("转换后照片地址：", args.result_dir)
    print("照片额外信息地址：", args.photo_info)
    print("照片请求地址(在本地浏览无需修改此项)：", args.request_dir)
    ci = ConvertImage()
    ci.do_convert_image(path=args.image_dir, new_path=args.result_dir, request_base_dir=args.request_dir,
                        photo_info=args.photo_info)
    print("恭喜您，批处理照片完成！")
    print("请稍等5秒，若浏览器未自动打开，请手动使用浏览器打开PhotoWall.html...")
    sleep(3)

