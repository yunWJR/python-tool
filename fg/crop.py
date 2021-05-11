from os import makedirs
from os.path import splitext, basename, isdir

import cv2

from file.file_util import image_files_from_folder


def handl_1():
    dir = "/Volumes/mac_data/2-pj/28-xztool/审计/法规/图片3"

    output_dir = dir + "/crop_out/"
    output_dir = "/Volumes/mac_data/2-pj/28-xztool/审计/法规/裁剪版/"
    if not isdir(output_dir):
        makedirs(output_dir)

    imgs_paths = image_files_from_folder(dir)

    for i, img_path in enumerate(imgs_paths):
        fname = basename(splitext(img_path)[0])

        img = cv2.imread(img_path)
        cropped = img[189:3321, 236:2245]  # 裁剪坐标为[y0:y1, x0:x1]
        cv2.imwrite(output_dir + fname + ".jpg", cropped, [int(cv2.IMWRITE_JPEG_QUALITY), 60])


def handl2():
    dir = "/Volumes/mac_data/2-pj/28-xztool/审计/法规/违反财经法规行为审计定性和处理处罚向导（修订版）上册/原始图片"

    output_dir = "/Volumes/mac_data/2-pj/28-xztool/审计/法规/违反财经法规行为审计定性和处理处罚向导（修订版）上册/裁剪版/"
    if not isdir(output_dir):
        makedirs(output_dir)

    imgs_paths = image_files_from_folder(dir)

    for i, img_path in enumerate(imgs_paths):
        fname = basename(splitext(img_path)[0])

        img = cv2.imread(img_path)
        rows, cols, a = img.shape
        # 这里的第一个参数为旋转中心，第二个为旋转角度，第三个为旋转后的缩放因子
        # 可以通过设置旋转中心，缩放因子以及窗口大小来防止旋转后超出边界的问题
        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), 180, 1)
        new_img = cv2.warpAffine(img, M, (cols, rows), borderValue=(255, 255, 255))  # M为上面的旋转矩阵

        cropped = new_img[0:2026, 106:1326]  # 裁剪坐标为[y0:y1, x0:x1]
        cv2.imwrite(output_dir + fname + ".jpg", cropped, [int(cv2.IMWRITE_JPEG_QUALITY), 100])


if __name__ == "__main__":
    handl2()
