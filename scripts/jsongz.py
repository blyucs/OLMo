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
import argparse
url_keywords = {
    ###### common start ####
    'en.wikipedia.org': 'Wikipedia',
    '.wikisource.org': 'Wikisource',
    '.cnn.com': 'CNN',
    ###### common end ####
    '.mdpi.com': 'MDPI',
    '.nytimes.com': 'NYTimes',
    '.archive.org': 'Archive',
    'journals.plos.org': 'PLOS',
    'serverfault.com': 'ServerFault',
    'archive.org': 'ArchiveOrg',
    'spectrum.ieee.org': 'IEEE',
    'nature.com': 'Nature',
    'techrepublic.com': 'TechRepublic',
    'wired.com': 'Wired',
    'physics.stackexchange.com': 'PhysicsStackExchange',
    'zdnet.com': 'ZDNet',
    'superuser.com': 'SuperUser',
    'studymoose.com': 'StudyMoose',
    'softmath.com': 'SoftMath',   # filter1  0 ~ 10000 OK    --- appended by 0~10000  below filters -- killed for full
##########################################
#### new  ----
    'mathoverflow.net': 'MathOverflow',
    'dailytech.com': 'DailyTech',
    'britannica.com': 'Britannica',
    'encyclopedia.com': 'Encyclopedia',
    'theregister.co.uk': 'TheRegister',
    'link.springer.com': 'Springer',
    'science.slashdot.org': 'ScienceSlashdot',
    'newworldencyclopedia.org': 'NewWorldEncyclopedia',
    'bookrags.com': 'BookRags',
    'boingboing.net': 'BoingBoing',
    'issuu.com': 'Issuu',
    'phys.org': 'PhysOrg',
    'healthunlocked.com': 'HealthUnlocked',
    'motls.blogspot.com': 'MotlsBlog',
    'genomebiology.biomedcentral.com': 'GenomeBiology',
# new  0----
    'theguardian.com': 'TheGuardian',
    'edition.cnn.com': 'EDITION_CNN',
    'ufdc.ufl.edu': 'UFDC',
    'enotes.com': 'ENotes',
##############################################
# new physics   --- all not filtered
    'mathwithbaddrawings.com': 'Mathwithbaddrawings',
    'nrich.maths.org': 'NrichMath',
    'plus.maths.org': 'PlusMath',
    'wiki.math.uwaterloo.ca': 'Uwaterloo',
    'encyclopediaofmath.org': 'MathEncyclopedia',
    'goodmath.org': 'GoodMath',
    'hackmath.net': 'HackMath',
    'math.columbia.edu': 'MathColum',
    'mathworks.com': 'MathSoftware',
    'purplemath.com': 'PurpleMath',
    'physicsworld.com': 'PhysicsWorld',
    'physicsforums.com': 'PhysicsForums',
    'physicsbuzz.physicscentral.com': 'PhysicsBuzz',
    'physicsoverflow.org': 'PhysicsOverflow',
    'math.stackexchange.com': 'MathStackExchange',
    'chemistry.stackexchange.com': 'ChemistryStackExchange',
    'chemistryworld.com': 'ChemistryWorld',
}

def setup_logging():
    logging.basicConfig(filename='jsonl_packing_errors.log', level=logging.INFO,
                        format='%(asctime)s:%(levelname)s:%(message)s')

def pack_jsonl_files_to_gz(directory, output_dir, max_size_gb=10, quality_thres=0.07):
    setup_logging()
    max_bytes = max_size_gb * 1024 * 1024 * 1024  # Convert GB to bytes
    current_size = 0
    part_num = 0
    total_size = 0

    # Extract the specific directory string for filename
    directory_name = os.path.basename(os.path.normpath(directory))

    # Ensure the directory exists
    output_path = os.path.join(output_dir, directory_name)
    os.makedirs(output_path, exist_ok=True)

    # Open the first output file
    filename = os.path.join(output_path, f'{directory_name}_part_{part_num}.json.gz')
    gzfile = gzip.open(filename, 'wt', encoding='utf-8')

    allowed_directories = set(url_keywords.values())
    # Directly list subdirectories of the main directory
    # subdirectories = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d)) and d in allowed_directories]
    # Directly list subdirectories of the main directory
    subdirectories = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]

    for dir_name in subdirectories:
        current_dir_path = os.path.join(directory, dir_name)
        for filename in os.listdir(current_dir_path):
            if filename.endswith('.jsonl'):
                file_path = os.path.join(current_dir_path, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    for line_number, line in enumerate(file, 1):
                        stripped_line = line.strip()
                        if not stripped_line:
                            continue  # Skip empty lines
                        try:
                            json_object = json.loads(stripped_line)
                            # if 'text' in json_object: # and json_object['fasttext_openhermes_reddit_eli5_vs_rw_v2_bigram_200k_train_prob'] > 0.15:
                            if 'text' in json_object and json_object['fasttext_openhermes_reddit_eli5_vs_rw_v2_bigram_200k_train_prob'] > quality_thres:
                                text_content = json_object['text']
                                minimal_json = json.dumps({"text": text_content})
                                if current_size + len(minimal_json.encode('utf-8')) + 1 > max_bytes:
                                    gzfile.close()
                                    part_num += 1
                                    gzfile = gzip.open(os.path.join(output_path, f'{directory_name}_part_{part_num}.json.gz'), 'wt', encoding='utf-8')
                                    current_size = 0  # Reset the size counter
                                gzfile.write(minimal_json + '\n')
                                current_size += len(minimal_json.encode('utf-8')) + 1
                                total_size += len(minimal_json.encode('utf-8')) + 1
                        except json.JSONDecodeError as e:
                            print(f"Error decoding JSON at {file_path}, line {line_number}: {e}")
    print(f"Total size {total_size}")
    gzfile.close()

# Example usage
# directory_path = '/home/lvbo/DCLM-data/Run_20241125-114153_0_to_2000'  # 设置你的文件夹路径
# directory_path = '/home/lvbo/DCLM-data/Run_20241125-114925_2000_to_4000'  # 设置你的文件夹路径
# directory_path = '/home/lvbo/DCLM-data/Run_20241125-223437_4000_to_6000'  # 设置你的文件夹路径
# # directory_path = '/home/lvbo/DCLM-data/Run_20241125-114153_0_to_2000'  # 设置你的文件夹路径
# # output_gz_path = '/home/lvbo/02_gz_data/'  # 设置输出文件的路径
# output_gz_path = '/home/lvbo/04_gz_all_common/'  # 设置输出文件的路径
# pack_jsonl_files_to_gz(directory_path, output_gz_path, max_size_gb=20)

def main():
    parser = argparse.ArgumentParser(description="Pack JSONL files into gzipped format.")
    parser.add_argument("directory", type=str, help="The directory with JSONL files to process.")
    parser.add_argument("output_dir", type=str, help="The directory to save the gzipped files.")
    parser.add_argument("--max_size_gb", type=int, default=10, help="Maximum size of each gzipped file in gigabytes.")
    parser.add_argument("--quality_thres", type=float, default=0.07, help="Maximum size of each gzipped file in gigabytes.")

    args = parser.parse_args()

    pack_jsonl_files_to_gz(args.directory, args.output_dir, args.max_size_gb, args.quality_thres)

if __name__ == "__main__":
    main()