from all_file import combine_all_file

if __name__ == "__main__":
    # dir = "/Volumes/mac_data/2-pj/18-cdhd/cdhd_server/cdhg-admin/src/main/java"
    dir = "/Users/yun/Downloads/Reimbursement"

    save_file = "/Users/yun/Downloads/a1.txt"

    java_ig = ['/**', '*', '*/', '//', '/*', '#pragma']

    # combine_all_file(dir, save_file, ['.java', '.kt'], java_ig)

    combine_all_file(dir, save_file, ['.m'], java_ig)
