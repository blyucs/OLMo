import os
import glob


def read_paths_from_files(directory):
    """
    Read file paths from all 'selected*.txt' files in the specified directory.
    """
    all_paths = set()
    # 使用glob模块查找所有符合条件的文件
    for file_path in glob.glob(os.path.join(directory, 'selected*.txt')):
        with open(file_path, 'r') as file:
            for line in file:
                # 去除空白字符并加入集合
                all_paths.add(line.strip())
    return all_paths


def compare_directories(dir1, dir2):
    """
    Compare two directories to find if there are any overlapping file paths in 'selected*.txt' files.
    """
    paths1 = read_paths_from_files(dir1)
    paths2 = read_paths_from_files(dir2)

    # 查找两个集合的交集
    intersection = paths1.intersection(paths2)

    if intersection:
        print("Found overlapping file paths:")
        for path in intersection:
            print(path)
    else:
        print("No overlapping file paths found.")


# 替换这些路径为实际的文件夹路径
directory1 = '/root/a100_nas_lvbo/peixunban/002754_lvbo/physics_filt/Run_20241125-114153_0_to_2000'
directory2 = '/root/a100_nas_lvbo/peixunban/002754_lvbo/physics_filt/Run_20241125-114925_4000_to_6000'
# directory2 = '/root/a100_nas_lvbo/peixunban/002754_lvbo/physics_filt/Run_20241123-152334_5001_to_10000'

compare_directories(directory1, directory2)
