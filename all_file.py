import os


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


def combine_all_file(dir, out_file, suffix, igs):
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
        if suffix is not None:
            if n.endswith(suffix) is False:
                continue

        print(n)
        sfp = open(n)
        ls = sfp.readlines()

        if igs is None or len(igs) == 0:
            fp.writelines(ls)
        else:
            for l in ls:
                ct = False
                for ig in igs:
                    if l.startswith(ig):
                        ct = True
                        break

                if ct:
                    continue

                fp.write(l)
