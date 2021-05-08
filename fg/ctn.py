#!/usr/bin/python
# -*- coding: UTF-8 -*-
from os import makedirs

from fg.rg import rg_zj, rg_sec3, rg_sec1, rg_sec2


def is_sec(line):
    rst = rg_zj(line)
    if rst is not None:
        return True

    rst = rg_sec1(line)
    if rst is not None:
        return True

    rst = rg_sec2(line)
    if rst is not None:
        return True

    rst = rg_sec3(line)
    if rst is not None:
        return True

    return False


# 目录格式化
def check_ml(file, out_file):
    fo = open(file, "r")

    fp = open(out_file, "w")

    ls = fo.readlines()

    nls = []
    for l in ls:
        l = l.strip()  # 去掉每行头尾空白

        if is_sec(l):
            nls.append(l)
        else:
            lastl = nls[len(nls) - 1]
            lastl = lastl + l
            nls[len(nls) - 1] = lastl

    for nl in nls:
        fp.write(nl)
        fp.write('\n')

    fp.close()


#  目录保存为 md 文件
def create_ctn_md(ml_file_md, ctn_file, out_file):
    mdmlf = open(ml_file_md, "r")
    ctnf = open(ctn_file, "r")

    fp = open(out_file, "w")

    ml_ls = mdmlf.readlines()
    ctn_ls = ctnf.readlines()

    ctn_l_i = 0

    ctn_num = 0
    cur_num = 0

    ml_l_i = 0
    for l in ml_ls:
        ml_l_i = ml_l_i + 1

        fp.write(l)

        if l == '\n':
            continue

        print(ml_l_i)

        if l.startswith("# "):
            k = rg_zj(l[2:]).group()

        # 详情
        if l.startswith("#### "):
            t = l[5:]

            find_num = None
            for num in range(ctn_l_i, len(ctn_ls)):
                if ctn_ls[num].startswith(t):
                    if num - ctn_l_i > 100:
                        print("%s-%s 匹配错误，内容大于100项。内容行号:%s" % (ml_l_i, t, ctn_l_i))
                        return

                    find_num = num
                    break

    fp.close()


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
        print("开始项： %s 未匹配" % z_key)
        return None

    if e_i is None:
        print("结束项： %s 未匹配" % z_end_key)
        return None

    return ctn_lines[s_i:e_i]


def ctnls_of_z3(z_key, z_end_key, ctn_lines):
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
        print("开始项： %s 未匹配" % z_key)
        return None

    if e_i is None:
        print("结束项： %s 未匹配" % z_end_key)
        return None

    return ctn_lines[s_i:e_i]


# 目录保存为 md 文件
def create_ctn(ml_file, ctn_file, out_dir):
    mlf = open(ml_file, "r")
    ml_ls = mlf.readlines()

    z_list = []
    z_key_list = []
    last_z = None
    for l in ml_ls:
        if rg_zj(l) is not None:
            print("目录章节：%s" % l)
            z_key_list.append(l)
            if last_z is not None:
                z_list.append(last_z)

            last_z = []

        last_z.append(l)

    z_list.append(last_z)

    ctnf = open(ctn_file, "r")
    ctn_ls = ctnf.readlines()
    z_ctn_g_lst = []

    for zi in range(len(z_key_list)):
        z_end_key = None
        if zi < len(z_key_list) - 1:
            z_end_key = z_key_list[zi + 1]

        rst = ctnls_of_z(z_key_list[zi], z_end_key, ctn_ls)
        if rst is None:
            return

        z_ctn_g_lst.append(rst)

    for z_k_i in range(len(z_key_list)):
        z_k = z_key_list[z_k_i]

        z_dir = out_dir + "/" + z_k
        makedirs(z_dir)

        z_file = z_dir + "/f.txt"
        fp = open(z_file, "w")
        z_ctn_g_lst_c = z_ctn_g_lst[z_k_i][1:]
        fp.writelines(z_ctn_g_lst_c)

        z_k_sl = z_list[z_k_i][1:]
        z1_k_list = []
        z3_k_list = []

        z1_dir_last = None
        for z1_k in z_k_sl:
            if rg_sec1(z1_k) is not None:
                z1_k_list.append(z1_k)
                z1_dir = out_dir + "/" + z_k + "/" + z1_k
                makedirs(z1_dir)
                z1_dir_last = z1_dir
            if rg_sec3(z1_k) is not None:
                z3_k_list.append(z1_k)

                z3_file = z1_dir_last + "/f.txt"
                fp = open(z3_file, "w")
                z3_lines = z_ctn_g_lst[z_k_i][1:]
                fp.writelines(z_ctn_g_lst[z_k_i][1:])


if __name__ == "__main__":
    ml_file = "/Volumes/mac_data/2-pj/28-xztool/审计/法规/格式化/目录_out.txt"
    ctn_file = "/Volumes/mac_data/2-pj/28-xztool/审计/法规/格式化/ctn.txt"
    out_dic = "/Volumes/mac_data/2-pj/28-xztool/审计/法规/格式化/ctn"

    create_ctn(ml_file, ctn_file, out_dic)
