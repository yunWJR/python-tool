#!/usr/bin/python
# -*- coding: UTF-8 -*-

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
def create_ml_md(file, out_file):
    fo = open(file, "r")

    fp = open(out_file, "w")

    ls = fo.readlines()

    for l in ls:
        if is_sec(l) is False:
            print("%s格式错误" % l)
            break

        if rg_zj(l) is not None:
            fp.write('# {}'.format(l))

        if rg_sec1(l) is not None:
            fp.write('## {}'.format(l))

        if rg_sec2(l) is not None:
            fp.write('### {}'.format(l))

        if rg_sec3(l) is not None:
            fp.write('#### {}'.format(l))

        fp.write('\n')

    fp.close()


if __name__ == "__main__":
    # ml_file = "/Volumes/mac_data/2-pj/28-xztool/审计/法规/格式化/目录.txt"
    # ml_file_out = "/Volumes/mac_data/2-pj/28-xztool/审计/法规/格式化/目录_out.txt"
    # check_ml(ml_file, ml_file_out)

    ml_file_out = "/Volumes/mac_data/2-pj/28-xztool/审计/法规/格式化/目录_out.txt"
    ml_file_out_md = "/Volumes/mac_data/2-pj/28-xztool/审计/法规/格式化/目录_out.md"
    create_ml_md(ml_file_out, ml_file_out_md)
