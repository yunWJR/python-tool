from os import makedirs
from os.path import splitext, basename, isdir

import cv2

from file.file_util import image_files_from_folder

if __name__ == "__main__":
    dir = "/Volumes/mac_data/2-pj/28-xztool/审计/法规/图片1"

    output_dir = dir + "/crop_out/"
    output_dir = "/Volumes/mac_data/2-pj/28-xztool/审计/法规/裁剪版"
    if not isdir(output_dir):
        makedirs(output_dir)

    imgs_paths = image_files_from_folder(dir)

    for i, img_path in enumerate(imgs_paths):
        fname = basename(splitext(img_path)[0])

        img = cv2.imread(img_path)
        cropped = img[189:3321, 236:2245]  # 裁剪坐标为[y0:y1, x0:x1]
        cv2.imwrite(output_dir + fname + ".jpg", cropped)
