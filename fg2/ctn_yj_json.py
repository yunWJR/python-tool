#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json

from fg.rg import rg_sec1, rg_sec2
# 目录保存为 md 文件
from fg2.fix_ctn import fix_ctn_file


def create_ctn(org_file, json_file):
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
            print("章节：%s" % l)
            cp = l
            continue

        # （一）
        if rg_sec2(l) is not None:
            if curItemTitle is not None:

                item = {"title": curItemTitle, "content": curItem}

                if cp is not None:
                    item["chapterName"] = cp
                items.append(item)

            rg_t = rg_sec2(l).group()

            curItemTitle = rg_t
            curItem = l[len(rg_t):]
            continue

            print("条：%s" % l)
            cp = l
            continue

        if curItem is None:
            curItem = l
        else:
            curItem = curItem + "\n" + l

    if curItem is not None:
        item = {"title": curItemTitle, "content": curItem}

        if cp is not None:
            item["chapterName"] = cp

        items.append(item)

    print(items)
    with open(json_file, 'w', encoding='utf-8') as file_obj:
        json.dump(items, file_obj, ensure_ascii=False)


if __name__ == "__main__":
    fix_ctn_file("/Users/yun/Downloads/意见",
                 "/Users/yun/Downloads/意见.txt")
    create_ctn("/Users/yun/Downloads/意见.txt", "/Users/yun/Downloads/意见-json.txt")
