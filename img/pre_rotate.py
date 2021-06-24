# 先通过hough transform检测图片中的图片，计算直线的倾斜角度并实现对图片的旋转
import math
import sys
from os import makedirs
from os.path import splitext, basename, isdir

import cv2
import numpy as np
from scipy import ndimage

from img.angle_contours import angle_by_contours
from util.file_util import image_files_from_folder


def rotate_forward(cv_img):
    rotate_angle = angle_by_contours(cv_img)
    if abs(rotate_angle) < 0.1:
        return cv_img, 0

    rotate_img = rotate_bound(cv_img.copy(), -rotate_angle)

    return rotate_img, rotate_angle


## 1、霍夫变换检测直线进行旋转
def rotate_by_hough_line(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # 霍夫变换
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 0)
    if lines is None:
        return img

    for rho, theta in lines[0]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
    if x2 == x1 or y1 == y2:
        return img

    t = float(y2 - y1) / (x2 - x1)
    rotate_angle = math.degrees(math.atan(t))
    if rotate_angle > 45:
        rotate_angle = -90 + rotate_angle
    elif rotate_angle < -45:
        rotate_angle = 90 + rotate_angle
    rotate_img = ndimage.rotate(img, rotate_angle)

    return rotate_img


## 2、傅立叶变化
def rotate_by_f(image):
    angle = get_minAreaRect(image)[-1]
    if (abs(angle) == 0):
        return image

    rotated = rotate_bound(image, angle)

    # cv2.putText(rotated, "angle: {:.2f} ".format(angle), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    return rotated


## 图片旋转
def rotate_bound(image, angle):
    # 获取宽高
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)

    # 提取旋转矩阵 sin cos
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # 计算图像的新边界尺寸
    nW = int((h * sin) + (w * cos))
    #     nH = int((h * cos) + (w * sin))
    nH = h

    # 调整旋转矩阵
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    return cv2.warpAffine(image, M, (nW, nH), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)


## 获取图片旋转角度
def get_minAreaRect(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    coords = np.column_stack(np.where(thresh > 0))
    return cv2.minAreaRect(coords)


## 3、矩形框检测
def rotate_by_area(image):
    angle = get_rotate_angle(image)
    if (abs(angle) == 0):
        return image

    r_img = get_rotated_image(image, angle)

    return r_img


# 获取旋转角度
def get_rotate_angle(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 转成单通道图片
    gray = cv2.bitwise_not(gray)  # 将上图颠倒黑白
    thresh = cv2.threshold(gray, 0, 255,
                           cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # 二值化，cv2.THRESH_BINARY（黑白二值），cv2.THRESH_OTSU自动判断最佳阈值（适合灰度图片有双峰的情况），使用cv2.THRESH_OTSU时阈值设置必须为0
    # cv2.threshold函数是有两个返回值的，（常用）第二个返回值：阈值处理后的图像，第一个返回值：得到图像的阈值

    coords = np.column_stack(np.where(thresh > 0))
    # print(coords)，所有黑色点的点集（数组型）

    area = cv2.minAreaRect(coords)
    # 返回一个rect：（最小外接矩形的中心（x，y），（宽度，高度），旋转角度）
    # rect[0]:中心坐标   rect[1][0]：矩形宽   rect[1][1]：矩形高    rect[2]：旋转角度θ
    # 旋转角度θ是水平轴（x轴）逆时针旋转，与碰到的矩形的第一条边的夹角。并且这个边的边长是width，另一条边边长是height。
    # 矩形的4个顶点坐标box, 通过函数 cv2.cv.BoxPoints() 获得
    angle = area[2]
    return angle


# 用矩阵旋转，字体不会变模糊。注意：warpAffine第三个参数（先列后行）。为防止信息丢失，W、H设置较大
def get_rotated_image(image, angle):
    (h, w) = image.shape[:2]
    M = cv2.getRotationMatrix2D((h // 2, w // 2), -angle, 1.0)
    sin = np.abs(M[0, 1])
    cos = np.abs(M[0, 0])
    a = np.maximum(h, w)
    W = int(a * sin + a * cos)
    H = int(a * cos + a * sin)
    M[0, 2] = W / 2 - w // 2
    M[1, 2] = H / 2 - h // 2
    rotated = cv2.warpAffine(image, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated


if __name__ == "__main__":
    input_dir = '/Users/yun/Downloads/test'

    o_rt_dir = input_dir + "_ocr_rotate"

    if not isdir(o_rt_dir):
        makedirs(o_rt_dir)

    imgs_paths = image_files_from_folder(input_dir)
    imgs_paths.sort()

    for i, img_path in enumerate(imgs_paths):
        fname = basename(splitext(img_path)[0])

        img = cv2.imread(img_path)

        r_img = rotate_by_area(img)

        r_f = '%s/%s_rt.jpg' % (o_rt_dir, fname)
        cv2.imwrite(r_f, r_img)

    sys.exit()
