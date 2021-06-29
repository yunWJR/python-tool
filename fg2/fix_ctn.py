import re

# 替换文字
fix_dict = {
    "\n\n": "\n",
    " ": "",
    " ": "",
    "　": "",
    "\t": "",
    "-": "一",
    "—": "一",
    "(": "（",
    ")": "）"
}


def fix_word(ctn: str):
    for dictKey in fix_dict.keys():
        ctn = ctn.replace(dictKey, fix_dict.get(dictKey))
    return ctn


def fix_ml_no(ctn: str):
    # 11, -> 11.
    pt = '[1-9][0-9]*\,'
    mt = re.match(pt, ctn)
    if mt is None:
        return ctn

    org = mt.group()
    n = org.replace(',', '.')

    ctn = ctn.replace(org, n)

    return ctn


# 内容修复
def fix_ctn_file(file: str, out_file: str):
    fo = open(file, "r")
    ls = fo.readlines()

    fp = open(out_file, "w")

    for l in ls:
        l = fix_ml_no(l)
        l = fix_word(l)

        fp.write(l)

    fo.close()
    fp.close()


def fix_ml_line(ctn: str):
    ctn = ctn.replace("H.", "11.")
    ctn = ctn.replace("…", "")
    ctn = ctn.replace("•", "")

    # 去除末尾数字
    pattern = re.compile(r'\d+')  # 查找数字

    h = ctn[:4]
    e = ctn[4:]

    nums = pattern.findall(e)
    for n in nums:
        e = e.replace(n, "")

    nl = h + e

    return nl


# 内容修正
if __name__ == "__main__":
    fix_ctn_file("/Users/yun/Downloads/1",
                 "/Users/yun/Downloads/1.txt")
