import zstandard as zstd
import json
import os
import logging
import random
import sys
# from item import physics_keywords_by_category
# Set up logging
logging.basicConfig(level=logging.ERROR)
from collections import defaultdict

# # 转换物理学家和物理名词列表为集合，并转为小写以支持不区分大小写的匹配
# physicist_set = set(physicist.lower() for physicist in physicists)
# term_set = set(term.lower() for term in physics_terms)
import shutil

def write_count_to_file(count, total_length, out_dir):
    with open(out_dir + "/wikipedia_counts.txt", "a") as f:
        f.write(f"{count},{total_length}\n")
def get_all_files(directory):
    all_files = []  # 存储所有文件的路径
    for root, dirs, files in os.walk(directory):
        for file in files:
            # if not (file.endswith("filelist_") or file.endswith("global1") or file.endswith("meta") or file.endswith("zst") or file.endswith("zstd")):
            if file.endswith("jsonl") or file.endswith("json"):
                file_path = os.path.join(root, file)  # 构造完整的文件路径
                all_files.append(file_path)  # 将文件路径添加到列表中
    return all_files

root_dir = "/root/a100_nas_lvbo/peixunban/public/datasets/dclm-baseline-1.0"
# out_dir = "/root/a100_nas_lvbo/peixunban/002754_lvbo/physics_filt/26000-27000_ALL"

def main(start_index, end_index, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    # 确保关键词文件夹存在
    filelist = get_all_files(root_dir)

    if start_index < 0 or end_index > len(filelist) or start_index > end_index:
        print("Invalid index range")
        return

    selected_files = filelist[start_index:end_index + 1]
    output_file_path = os.path.join(out_dir, f"selected_files_{start_index}_to_{end_index}.txt")
    with open(output_file_path, 'w') as file:
        for path in selected_files:
            file.write(path + '\n')

    total_files = len(selected_files)
    for i, file_path in enumerate(selected_files):
        base_name = os.path.basename(file_path)
        # 生成一个较大的随机数
        random_number = random.randint(1000000, 9999999)
        unique_filename = f"{base_name.split('.')[0]}_{random_number}.{base_name.split('.')[-1]}"
        output_file_path = os.path.join(out_dir, unique_filename)
        shutil.copy(file_path, output_file_path)
        # 计算并打印进度百分比
        progress_percent = ((i + 1) / total_files) * 100
        print(f"Progress: {progress_percent:.2f}% - Processing file {i + 1}/{total_files} (Range: {start_index} to {end_index})")


    print(f"Processed files from index {start_index} to {end_index}. ")
    # return total_count, total_text_length
    return

if __name__ == "__main__":
    # if len(sys.argv) != 3:
    #     print("Usage: python script.py <start_index> <end_index>")
    #     sys.exit(1)
    start_index = int(sys.argv[1])
    end_index = int(sys.argv[2])
    out_dir = str(sys.argv[3])
    # out_dir = "/root/a100_nas_lvbo/peixunban/002754_lvbo/physics_filt/test"
    # start_index = 26000
    # end_index = 27000
    # result = main(start_index, end_index, out_dir)
    main(start_index, end_index, out_dir)
    # sys.exit(result)
