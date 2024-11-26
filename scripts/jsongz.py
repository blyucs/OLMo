import json
import gzip

# # 读取.jsonl文件
# def process_jsonl_to_jsonl_gz(input_file_path, output_file_path):
#     with open(input_file_path, 'r', encoding='utf-8') as input_file:
#         with gzip.open(output_file_path, 'wt', encoding='utf-8') as output_file:
#             for line_number, line in enumerate(input_file, 1):
#                 stripped_line = line.strip()
#                 if not stripped_line:  # 跳过空行
#                     print(f"Skipping empty line at {line_number}")
#                     continue
#                 try:
#                     json.loads(stripped_line)  # 检查JSON格式是否正确
#                     output_file.write(stripped_line+'\n')  # 直接写入字符串
#                 except json.JSONDecodeError as e:
#                     print(f"Error decoding JSON at line {line_number}: {e}")
#
# # 使用的文件路径
# jsonl_file_path = '/workspace/lvbo_a100/peixunban/002754_lvbo/physics_filt/4-4-NCBI_1.jsonl'
# json_gz_file_path = '/workspace/lvbo_a100/peixunban/002754_lvbo/physics_filt/4-4-NCBI_1.json.gz'
#
# # 转换过程
# process_jsonl_to_jsonl_gz(jsonl_file_path, json_gz_file_path)
import gzip
import os
import json

def pack_jsonl_files_to_gz(directory, output_file_path):
    with gzip.open(output_file_path, 'wt', encoding='utf-8') as gzfile:
        # 递归遍历文件夹
        for root, dirs, files in os.walk(directory):
            for filename in files:
                if filename.endswith('.jsonl'):
                    file_path = os.path.join(root, filename)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        for line_number, line in enumerate(file, 1):
                            stripped_line = line.strip()
                            if not stripped_line:  # 检查是否为空行
                                continue  # 空行则跳过
                            try:
                                json_object = json.loads(stripped_line)  # 解析每一行的JSON
                                json_string = json.dumps(json_object)  # 将JSON对象转换为字符串
                                gzfile.write(json_string + '\n')  # 写入压缩文件
                            except json.JSONDecodeError as e:
                                print(f"Error decoding JSON at {file_path}, line {line_number}: {e}")


# 使用示例
directory_path = '/workspace/lvbo_a100/peixunban/002754_lvbo/physics_filt/Run_20241123-125643_0_to_5000/Wikipedia'  # 设置你的文件夹路径
output_gz_path = '/workspace/lvbo_a100/peixunban/002754_lvbo/physics_filt/Run_20241123-125643_0_to_5000/output_file.json.gz'  # 设置输出文件的路径
pack_jsonl_files_to_gz(directory_path, output_gz_path)
