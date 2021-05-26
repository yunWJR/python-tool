#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json

from fg.rg import rg_zj, rg_tiao


# 目录保存为 md 文件
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

        if rg_zj(l) is not None:
            print("目录章节：%s" % l)
            cp = l
            continue

        if rg_tiao(l) is not None:
            if curItemTitle is not None:

                item = {"title": curItemTitle, "content": curItem}

                if cp is not None:
                    item["chapterName"] = cp
                items.append(item)

            rg_t = rg_tiao(l).group()

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
    create_ctn("/Users/yun/Downloads/会计法-fix.txt", "/Users/yun/Downloads/会计法-json.txt")
