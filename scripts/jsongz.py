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
import json
import os
import logging

def setup_logging():
    logging.basicConfig(filename='jsonl_packing_errors.log', level=logging.ERROR,
                        format='%(asctime)s:%(levelname)s:%(message)s')

def pack_jsonl_files_to_gz(directory, output_dir, max_size_gb=10):
    setup_logging()
    max_bytes = max_size_gb * 1024 * 1024 * 1024  # Convert GB to bytes
    current_size = 0
    part_num = 0

    # Extract the specific directory string for filename
    directory_name = os.path.basename(os.path.normpath(directory))
    
    # Open the first output file
    gzfile = gzip.open(os.path.join(output_dir, f'{directory_name}/{directory_name}_part_{part_num}.json.gz'), 'wt', encoding='utf-8')
    
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.jsonl'):
                file_path = os.path.join(root, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    for line_number, line in enumerate(file, 1):
                        stripped_line = line.strip()
                        if not stripped_line:
                            continue  # Skip empty lines
                        try:
                            json_object = json.loads(stripped_line)
                            if 'text' in json_object:
                                text_content = json_object['text']
                                minimal_json = json.dumps({"text": text_content})
                                if current_size + len(minimal_json.encode('utf-8')) + 1 > max_bytes:
                                    gzfile.close()
                                    part_num += 1
                                    gzfile = gzip.open(os.path.join(output_dir, f'{directory_name}/{directory_name}_part_{part_num}.json.gz'), 'wt', encoding='utf-8')
                                    current_size = 0  # Reset the size counter
                                gzfile.write(minimal_json + '\n')
                                current_size += len(minimal_json.encode('utf-8')) + 1
                            else:
                                logging.error(f"Missing 'text' field at {file_path}, line {line_number}")
                        except json.JSONDecodeError as e:
                            logging.error(f"Error decoding JSON at {file_path}, line {line_number}: {e}")

    gzfile.close()

# Example usage
directory_path = '/home/lvbo/DCLM-data/Run_20241125-114153_0_to_2000/'  # 设置你的文件夹路径
output_gz_path = '/home/lvbo/01_gz_data/'  # 设置输出文件的路径
pack_jsonl_files_to_gz(directory_path, output_gz_path, max_size_gb=10)

