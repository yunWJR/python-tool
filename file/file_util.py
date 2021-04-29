from glob import glob


def image_files_from_folder(folder, upper=True):
    extensions = ['jpg', 'jpeg', 'png']
    img_files = []
    for ext in extensions:
        img_files += glob('%s/*.%s' % (folder, ext))
        if upper:
            img_files += glob('%s/*.%s' % (folder, ext.upper()))
    return img_files


