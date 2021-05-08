#!/usr/bin/python
# -*- coding: UTF-8 -*-
from os import makedirs

from fg.rg import rg_zj, rg_sec3, rg_sec1, rg_sec2


def ctnls_of_z(z_key, z_end_key, ctn_lines):
    s_i = None
    e_i = None

    for li in range(len(ctn_lines)):
        l = ctn_lines[li]
        if l == z_key:
            s_i = li
            continue

        if z_end_key is not None:
            if l == z_end_key:
                e_i = li

    if z_end_key is None:
        e_i = len(ctn_lines) - 1

    if s_i is None:
        print("错误：：开始项： %s 未匹配" % z_key)
        return None

    if e_i is None:
        print("错误：：结束项： %s 未匹配" % z_end_key)
        return None

    return ctn_lines[s_i:e_i]


# 目录保存为 md 文件
def create_ctn(p_dic, type):
    # print(p_dic)

    mlf = open(p_dic + "/目录.txt", "r")
    ml_ls = mlf.readlines()

    ctnf = open(p_dic + "/内容.txt", "r")
    ctn_ls = ctnf.readlines()

    z_list = []
    z_key_list = []
    last_z = None
    for l in ml_ls:
        if (type == 0 and rg_zj(l) is not None) or (type == 1 and rg_sec1(l) is not None) or (
                type == 3 and rg_sec3(l) is not None):
            # print("目录章节：%s" % l)
            z_key_list.append(l)
            if last_z is not None:
                z_list.append(last_z)

            last_z = []

        if last_z is None:
            if rg_sec2(l) is not None:
                continue

            print("ERROR:  " + l + "")
            return
        last_z.append(l)

    z_list.append(last_z)

    dic_list = []

    for zi in range(len(z_key_list)):
        z_end_key = None
        if zi < len(z_key_list) - 1:
            z_end_key = z_key_list[zi + 1]

        rst = ctnls_of_z(z_key_list[zi], z_end_key, ctn_ls)
        if rst is None:
            return

        z_k = z_key_list[zi].strip()
        z_dir = p_dic + "/" + z_k
        makedirs(z_dir)

        dic_list.append(z_dir)

        z_ml_file = z_dir + "/目录.txt"
        f_ml = open(z_ml_file, "w")
        f_ml.writelines(z_list[zi][1:])

        z_file = z_dir + "/内容.txt"
        fp = open(z_file, "w")
        fp.writelines(rst[1:])

        if type == 3:
            z_file = z_dir + "/内容.md"
            fp = open(z_file, "w")
            fp.writelines(rst[1:])

    return dic_list


if __name__ == "__main__":
    p_dic = "/Volumes/mac_data/2-pj/28-xztool/审计/法规/格式化/ctn"
    rst_dir = create_ctn(p_dic, 0)

    for d1 in rst_dir:
        rst_d3 = create_ctn(d1, 1)
        for d3 in rst_d3:
            create_ctn(d3, 3)
