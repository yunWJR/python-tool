from all_file import combine_all_file

if __name__ == "__main__":
    dir = "/Volumes/mac_data/2-pj/99-alarm/alarm-server/alarm-capi/src/main/java/com/kd/alarm/capi"

    save_file = "/Users/yun/Downloads/a1.txt"

    java_ig = ['/**', ' *']

    combine_all_file(dir, save_file, '.java', java_ig)
