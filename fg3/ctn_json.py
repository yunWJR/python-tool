#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json

from fg.rg import rg_zj, rg_sec1, rg_sec3


# 目录保存为 md 文件


def get_md_file(item_file):
    mlf = open(item_file, "r")
    ml_ls = mlf.readlines()

    ctn = ''

    for l in ml_ls:
        l = l.replace("\n", "")
        l = l.replace("## ", "")
        if len(l) == 0:
            continue

        ctn = ctn + "\n" + l

    return ctn


def create_ctn(org_dir, json_file):
    ml_file = org_dir + '/目录.txt'

    cp = None
    sc = None

    items = []

    curItemTitle = None
    curItem = None

    mlf = open(ml_file, "r")
    ml_ls = mlf.readlines()

    for l in ml_ls:
        if l.endswith("\n"):
            l = l[:len(l) - 1]

        if rg_zj(l) is not None:
            print("目录章：%s" % l)
            cp = l
            continue
        if rg_sec1(l) is not None:
            print("目录节：%s" % l)
            sc = l
            continue

        if rg_sec3(l) is not None:
            item_file = org_dir + "/" + cp + "/" + sc + "/" + l + "/内容格式化.md"

            item_ctn = get_md_file(item_file)

            item = {"title": l, "content": item_ctn, "chapterName": cp, "sectionName": sc}
            items.append(item)

    print(items)
    with open(json_file, 'w', encoding='utf-8') as file_obj:
        json.dump(items, file_obj, ensure_ascii=False)


if __name__ == "__main__":
    create_ctn("/Volumes/mac_data/2-pj/28-xztool/审计/法规/违反财经法规行为审计定性和处理处罚向导（修订版）下册/核对内容", "/Users/yun/Downloads/1-json.txt")
