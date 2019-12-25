from src.ConvertImage import ConvertImage

if __name__=='__main__':
    print("*******************照片转换程序***********************")
    print("*******************制作：小麦冬***********************")
    print("**该程序用于将体积较大的原始照片转换为适合网页展示的缩略图和大图 ******")
    print("*************-并生成网页展示需要的照片数据-*****************")
    print("************请根据提示进行以下操作************************")
    print("******请输入原始照片地址（按Enter使用默认地址\"image\"）*********")
    file_path = input()
    if file_path.strip() == '':
        file_path = "image"
    print("*请输入转换后的照片将保存的地址（按Enter使用默认地址\"image\"）***")
    new_path = input()
    print("*****如果您打算在本地浏览照片，请直接按Enter，若不是，请输入网址****")
    print("*比如:photo.xiaomaidong.com/test/，表示将在小麦冬上搭载网页*")
    request_base_dir = input()
    ci = ConvertImage()
    ci.do_convert_image(file_path.strip(), new_path=new_path.strip(), request_base_dir=request_base_dir.strip())
