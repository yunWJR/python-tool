import math
import sys

import cv2
import numpy as np


def rotate_bound_test(image, angle):
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


def angle_by_contours(cv_img):
    show_img = False

    # 用于检测直线
    canny = True

    cv_img = cv2.GaussianBlur(cv_img, (3, 3), 0)

    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)

    k_size = None
    edges_img = None
    if canny:
        k_size = (20, 1)
        edges_img = cv2.Canny(gray, 50, 150, apertureSize=3)
        if show_img:
            cv2.imshow("canny-edges_img", edges_img)
    else:
        k_size = (20, 2)
        edges_img = cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize=3)
        if show_img:
            cv2.imshow("sobel-edges_img", edges_img)

    ret, binary = cv2.threshold(edges_img, 75, 255, cv2.THRESH_BINARY)

    if show_img:
        cv2.imshow("binary", binary)

    ## 图像的膨胀
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, k_size)  # 矩形结构
    dst = cv2.dilate(binary, kernel, iterations=2)

    if show_img:
        cv2.imshow("dst", dst)

    contours, hierarchy = cv2.findContours(dst, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    if show_img:
        ct_img = cv_img.copy()
        cv2.drawContours(ct_img, contours, -1, (0, 0, 255), 2)
        cv2.imshow("ct_img", ct_img)

    org_rect_list = []
    rect_list = []
    angle_list = []
    line_list = []

    i_h, i_w = cv_img.shape[:2]
    i_x_min_p = 0.02
    i_x_max_p = 1 - i_x_min_p
    for i, ct in enumerate(contours):
        rect = cv2.minAreaRect(ct)

        width = int(rect[1][0])
        height = int(rect[1][1])

        angle = rect[2]

        if angle < -45:
            width = int(rect[1][1])
            height = int(rect[1][0])
            angle = 90 + angle

        if show_img:
            box = cv2.boxPoints(rect)  # cv2.boxPoints(rect) for OpenCV 3.x 获取最小外接矩形的4个顶点坐标
            box = np.int0(box)  # [ [x0,y0], [x1,y1], [x2,y2], [x3,y3] ]
            org_rect_list.append(box)

        # 排除不规则形状
        if width < height * 3:
            continue

        box = cv2.boxPoints(rect)  # cv2.boxPoints(rect) for OpenCV 3.x 获取最小外接矩形的4个顶点坐标
        box = np.int0(box)  # [ [x0,y0], [x1,y1], [x2,y2], [x3,y3] ]

        # 排除四周的
        box_x = [box[0][0], box[1][0], box[2][0], box[3][0]]
        box_x_min = min(box_x)
        box_x_max = max(box_x)

        # 排除边缘
        if box_x_min < i_w * i_x_min_p or box_x_max > i_w * i_x_max_p:
            continue

        box_y = [box[0][1], box[1][1], box[2][1], box[3][1]]
        box_y_min = min(box_y)
        box_y_max = max(box_y)

        # 排除边缘
        if box_y_min < i_h * i_x_min_p or box_y_max > i_h * i_x_max_p:
            continue

        # 是线条
        if height < 10:
            if width > i_w * 0.5:
                line_list.append(box)
                # continue
            else:
                continue

        rect_list.append(box)

        item = (float(height) / width, angle)
        angle_list.append(item)

    if show_img:
        rect_org_img = cv_img.copy()
        cv2.drawContours(rect_org_img, org_rect_list, -1, (0, 255, 255), 1)
        cv2.imshow("rect_org_img", rect_org_img)

        rect_img = cv_img.copy()
        cv2.drawContours(rect_img, rect_list, -1, (0, 0, 255), 2)
        cv2.imshow("rect_img", rect_img)

        rect_line_img = cv_img.copy()
        cv2.drawContours(rect_line_img, line_list, -1, (0, 122, 122), 2)
        cv2.imshow("rect_line_img", rect_line_img)

        cv2.waitKey(0)

    r_ag = 0
    if len(angle_list) >= 4:
        limit = int(len(angle_list) * 0.7)
        if limit < 4:
            limit = len(angle_list)

        angle_list = sorted(angle_list, key=lambda x: x[0])

        valid_a_list = angle_list[:limit]

        v_list = []

        max_a = -180
        max_id = -1
        min_a = 180
        min_id = -1
        for i, ag in enumerate(valid_a_list):
            ag_v = ag[1]
            v_list.append(ag_v)
            if ag_v > max_a:
                max_a = ag_v
                max_id = i
            elif ag_v < min_a:
                min_a = ag_v
                min_id = i

        # 移除最大、最小值
        if max_id > min_id:
            if max_id >= 0:
                v_list.pop(max_id)
            if min_id >= 0:
                v_list.pop(min_id)
        elif min_id > max_id:
            if min_id >= 0:
                v_list.pop(min_id)
            if max_id >= 0:
                v_list.pop(max_id)

        ag_mean = np.mean(v_list)

        per = 10
        ag_mean_per = abs(ag_mean / (2 * per))

        best_ag = ag_mean
        best_ag_std = None
        for i in range(int(per / 2)):
            add_ag = ag_mean + i * ag_mean_per
            var_a = var_mean(v_list, add_ag)
            if best_ag_std is None or best_ag_std > var_a:
                best_ag_std = var_a
                best_ag = add_ag

            if i == 0:
                continue

            sub_ag = ag_mean - i * ag_mean_per
            var_s = var_mean(v_list, sub_ag)
            if best_ag_std is None or best_ag_std > var_s:
                best_ag_std = var_s
                best_ag = sub_ag

        r_ag = best_ag

    return r_ag


def var_mean(items, mean_v):
    if len(items) <= 0:
        return 0

    if len(items) == 1:
        return mean_v

    var = 0
    for i, it in enumerate(items):
        v_i = math.pow((it - mean_v), 2)
        var += v_i

    std = math.sqrt(var / (len(items)))
    std_m = abs(std / mean_v)
    print('var_mean:%s   %s   %s   %s' % (mean_v, std, std_m, var))

    return std_m


if __name__ == "__main__":
    img = cv2.imread('/Users/yun/Downloads/test.jpg')
    r_ag = angle_by_contours(img)
    print(r_ag)

    rotate_img = rotate_bound_test(img.copy(), -r_ag)

    cv2.imshow("org_img", img)
    cv2.imshow("rotate_img", rotate_img)

    cv2.waitKey(0)

    sys.exit()
