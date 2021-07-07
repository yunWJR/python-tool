#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json

from fg.rg import rg_sec1, rg_sec2, rg_zj, rg_tiao, rg_sec3_1
# 目录保存为 md 文件
from fg2.fix_ctn import fix_ctn_file


def reform_base(l):
    if len(l) == 0 or l == '#':
        return ''

    return l


def create_ctn(org_file, json_file, type):
    no_cp = True
    cp = None
    cp_items = []
    cp_list = []

    items = []

    mlf = open(org_file, "r")
    ml_ls = mlf.readlines()

    allData = {}

    i = 0
    for l in ml_ls:
        if l.endswith("\n"):
            l = l[:len(l) - 1]

        i = i + 1
        if i == 1:
            allData['name'] = reform_base(l)
        if i == 2:
            allData['pubdate'] = reform_base(l)
        if i == 3:
            allData['fileNo'] = reform_base(l)
        if i == 4:
            allData['author'] = reform_base(l)

        if i <= 4:
            continue

        rg_s1 = None
        if type == 1:
            # 第一章
            rg_s1 = rg_zj(l)
        else:
            # 一、
            rg_s1 = rg_sec1(l)
            # 第一条
            # rg_s1 = rg_tiao(l)
        if rg_s1 is not None:
            if cp is not None:
                cpMap = {"cp": cp, "cp_items": cp_items}
                cp_list.append(cpMap)

                cp = None
                cp_items = []

            print("章节：%s" % l)
            cp = l

            continue

        if cp is not None or no_cp:
            cp_items.append(l)

    if cp is not None:
        cpMap = {"cp": cp, "cp_items": cp_items}
        cp_list.append(cpMap)
    else:
        cpMap = {"cp": '', "cp_items": cp_items}
        cp_list.append(cpMap)

    # 二次分组
    for cpMap in cp_list:
        cp = cpMap.get('cp')
        cp_items = cpMap.get('cp_items')

        sec = None
        cur_ctn = None
        for cp_item in cp_items:

            rg_s1 = None
            if type == 1:
                # 第一条
                rg_s1 = rg_tiao(cp_item)
            else:
                # （一）
                # rg_s1 = rg_sec2(cp_item)
                # 1、
                # rg_s1 = rg_sec3_1(cp_item)
                # 第一条
                rg_s1 = rg_tiao(cp_item)
            if rg_s1 is not None:
                if sec is not None:
                    item = {"title": sec, "content": cur_ctn, "chapterName": cp}
                    items.append(item)

                rg_t = rg_s1.group()

                sec = rg_t
                cur_ctn = cp_item[len(rg_t):]
                continue

            if cur_ctn is None:
                cur_ctn = cp_item
            else:
                cur_ctn = cur_ctn + "\n" + cp_item

        if sec is None:
            item = {"title": "", "content": cur_ctn, "chapterName": cp}
            items.append(item)
        else:
            item = {"title": sec, "content": cur_ctn, "chapterName": cp}
            items.append(item)

    allData['itemList'] = items
    allData['type'] = type
    print(allData)
    with open(json_file, 'w', encoding='utf-8') as file_obj:
        json.dump(allData, file_obj, ensure_ascii=False)


# 只有一级标题
def create_ctn_s1(org_file, json_file):
    cp = None

    items = []

    curItemTitle = None
    curItem = None

    mlf = open(org_file, "r")
    ml_ls = mlf.readlines()

    for l in ml_ls:
        if l.endswith("\n"):
            l = l[:len(l) - 1]

        # 一、
        if rg_sec1(l) is not None:
            if cp is not None:
                item = {"chapterName": cp, "content": curItem}
                items.append(item)
                curItem = None

            print("章节：%s" % l)
            cp = l
            continue

        if curItem is None:
            curItem = l
        else:
            curItem = curItem + "\n" + l

    if curItem is not None:
        item = {"chapterName": cp, "content": curItem}

        items.append(item)

    print(items)
    with open(json_file, 'w', encoding='utf-8') as file_obj:
        json.dump(items, file_obj, ensure_ascii=False)


if __name__ == "__main__":
    # 1-法规；3-意见
    type = 3

    fix_ctn_file("/Users/yun/Downloads/意见",
                 "/Users/yun/Downloads/意见.txt")

    create_ctn("/Users/yun/Downloads/意见.txt", "/Users/yun/Downloads/意见-json.txt", type)
