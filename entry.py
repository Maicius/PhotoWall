from ConvertImage import ConvertImage
import argparse

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
    print("原始照片地址：", args.image_dir)
    print("转换后照片地址：", args.result_dir)
    print("照片额外信息地址：", args.photo_info)
    print("照片请求地址(在本地浏览无需修改此项)：", args.request_dir)
    ci = ConvertImage()
    ci.do_convert_image(path=args.image_dir, new_path=args.result_dir, request_base_dir=args.request_dir,
                        photo_info=args.photo_info)
    print("批处理照片完成，请用浏览器打开PhotoWall.html即可查看照片墙")
    print("按任意键离开程序...")
    input()

