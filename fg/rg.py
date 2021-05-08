import re

dx = '[一二三四五六七八九十]+'


# 第一章
def rg_zj(str):
    pt = '第{}章'.format(dx)
    return re.match(pt, str)


# 一、
def rg_sec1(str):
    pt = '{}、'.format(dx)
    return re.match(pt, str)


# （一）
def rg_sec2(str):
    pt = '（{}）'.format(dx)
    return re.match(pt, str)


# 11.
def rg_sec3(str):
    pt = '[1-9][0-9]*\.'
    return re.match(pt, str)


#   123123  -末尾页码数字
def rg_end1(str):
    pt = '\s+[1-9][0-9]*\s*'
    return re.match(pt, str)


if __name__ == "__main__":
    rst = rg_zj('第一章固定资产投资审计类\n')
    print(rst)

    rst = rg_sec1("一、大事发生")
    print(rst)

    rst = rg_sec3("123123.sdfdsaf")
    print(rst)
