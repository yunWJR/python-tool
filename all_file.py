import os


# 软著代码整合

def all_file_of_dir(dir, files):
    '''
    目录下所有文件
    :param dir:
    :param files:
    :return:
    '''
    get_dir = os.listdir(dir)

    for i in get_dir:

        sub_dir = os.path.join(dir, i)

        if os.path.isdir(sub_dir):

            all_file_of_dir(sub_dir, files)

        else:
            files.append(os.path.join(dir, i))


def isStartWith(line, igs):
    nl = line.lstrip()
    for ig in igs:
        if nl.startswith(ig):
            return True

    return False


def combine_all_file(dir, out_file, suffixs, igs):
    '''
    结合所有文件
    :param dir:
    :param out_file:
    :return:
    '''
    fp = open(out_file, "w")

    files = []
    all_file_of_dir(dir, files)

    for n in files:
        if suffixs is not None:
            fd = False
            for sf in suffixs:
                if n.endswith(sf) is True:
                    fd = True
                    break

            if fd is False:
                continue

        print(n)

        if n.lower().find("test") >= 0:
            print("skit test")
            continue

        sfp = open(n)
        ls = sfp.readlines()

        if igs is None or len(igs) == 0:
            fp.writelines(ls)
        else:
            for l in ls:
                if isStartWith(l, igs):
                    continue

                fp.write(l)
