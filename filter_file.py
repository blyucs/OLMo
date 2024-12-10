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
import portalocker

# URL关键词到文件夹的映射
url_keywords = {
#     'en.wikipedia.org': 'Wikipedia',
#     '.wikisource.org': 'Wikisource',
#     '.cnn.com': 'CNN',
#     '.mdpi.com': 'MDPI',
#     '.nytimes.com': 'NYTimes',
#     '.archive.org': 'Archive',
#     'stackoverflow.com': 'StackOverflow',
#     'journals.plos.org': 'PLOS',
#     'serverfault.com': 'ServerFault',
#     'programmers.stackexchange.com': 'StackExchange',
#     'archive.org': 'ArchiveOrg',
#     'hackaday.com': 'Hackaday',
#     'spectrum.ieee.org': 'IEEE',
#     'forum.arduino.cc': 'ArduinoForum',
#     'nature.com': 'Nature',
#     'techrepublic.com': 'TechRepublic',
#     'bmcbioinformatics.biomedcentral.com': 'BMCBioinformatics',
#     'meta.stackoverflow.com': 'MetaStackOverflow',
#     'beta.slashdot.org': 'SlashdotBeta',
#     'wired.com': 'Wired',
#     'bmcgenomics.biomedcentral.com': 'BMCGenomics',
#     'physics.stackexchange.com': 'PhysicsStackExchange',
#     'zdnet.com': 'ZDNet',
#     'ncbi.nlm.nih.gov': 'NCBI',
#     'superuser.com': 'SuperUser',
#     'linux.slashdot.org': 'LinuxSlashdot',
#     'studymoose.com': 'StudyMoose',
#     'pcworld.com': 'PCWorld',
#     'tex.stackexchange.com': 'TexStackExchange',
#     'softmath.com': 'SoftMath',   # filter1  0 ~ 10000 OK    --- appended by 0~10000  below filters -- killed for full
# ##########################################
# #### new  ----
#     'mathoverflow.net': 'MathOverflow',
#     'dailytech.com': 'DailyTech',
#     'britannica.com': 'Britannica',
#     'encyclopedia.com': 'Encyclopedia',
#     'theregister.co.uk': 'TheRegister',
#     'link.springer.com': 'Springer',
#     'science.slashdot.org': 'ScienceSlashdot',
#     'biomedsearch.com': 'BiomedSearch',
#     'newworldencyclopedia.org': 'NewWorldEncyclopedia',
#     'bookrags.com': 'BookRags',
#     'boingboing.net': 'BoingBoing',
#     'issuu.com': 'Issuu',
#     'github.com': 'GitHub',
#     'phys.org': 'PhysOrg',
#     'forums.webmd.com': 'WebMD',
#     'healthunlocked.com': 'HealthUnlocked',
#     'motls.blogspot.com': 'MotlsBlog',
#     'genomebiology.biomedcentral.com': 'GenomeBiology',
#     'infoq.com': 'InfoQ',
#     'realclimate.org': 'RealClimate',
# # new  0----
#     'theguardian.com': 'TheGuardian',
#     'edition.cnn.com': 'EDITION_CNN',
#     'ufdc.ufl.edu': 'UFDC',
#     'enotes.com': 'ENotes',
#     'pubmedcentralcanada.ca': 'PubMedCentralCanada',   #filter2 10000~27000 OK   --- appended by 10000~27000 below filter  --- killed for full
# ##############################################
# # new physics   --- all not filtered
#     'mathwithbaddrawings.com': 'Mathwithbaddrawings',
#     'nrich.maths.org': 'NrichMath',
#     'plus.maths.org': 'PlusMath',
#     'wiki.math.uwaterloo.ca': 'Uwaterloo',
#     'encyclopediaofmath.org': 'MathEncyclopedia',
#     'goodmath.org': 'GoodMath',
#     'hackmath.net': 'HackMath',
#     'math.columbia.edu': 'MathColum',
#     'mathworks.com': 'MathSoftware',
#     'purplemath.com': 'PurpleMath',
#     'physicsworld.com': 'PhysicsWorld',
#     'physicsforums.com': 'PhysicsForums',
#     'physicsbuzz.physicscentral.com': 'PhysicsBuzz',
#     'physicsoverflow.org': 'PhysicsOverflow',
#     'math.stackexchange.com': 'MathStackExchange',
#     'chemistry.stackexchange.com': 'ChemistryStackExchange',
#     'chemistryworld.com': 'ChemistryWorld',
# # bio 1
#     'bmcvebiol.biomedcentral.com': 'VeterinaryBiology',
#     'bio.net': 'BioNet',
#     'bio-medicine.org': 'BioMedicine',
#     'biology.stackexchange.com': 'BiologyStackExchange',
#     'bmcsystbiol.biomedcentral.com': 'SystemsBiology',
#     'www.biographi.ca': 'BiographiCA',
#     'bmcplantbiol.biomedcentral.com': 'PlantBiology',
#     'bmcneurosci.biomedcentral.com': 'Neuroscience',
#     'bmcmicrobiol.biomedcentral.com': 'Microbiology',
#     'bmcpublichealth.biomedcentral.com': 'PublicHealth',
#     'bmccancer.biomedcentral.com': 'CancerResearch',
#     'astrobio.net': 'AstroBiology',
#     'biotechnologyforbiofuels.biomedcentral.com': 'BioTechForBiofuels',
#     'biology-online.org': 'BiologyOnline',
#     'arthritis-research.biomedcentral.com': 'ArthritisResearch',
#     'biologos.org': 'BioLogos',
# # bio 2
#     'parasitesandvectors.biomedcentral.com': 'ParasitesVectors',
#     'bmcresearchnotes.biomedcentral.com': 'ResearchNotes',
#     'dubiousquality.blogspot.com': 'DubiousQuality',
#     'translational-medicine.biomedcentral.com': 'TranslationalMedicine',
#     'ploscompbiol.org': 'PLOSCompBiol',
#     'bmcmedicine.biomedcentral.com': 'BMCMedicine',
#     'malariajournal.biomedcentral.com': 'MalariaJournal',
#     'microbialcellfactories.biomedcentral.com': 'MicrobialCellFactories',
#     'virologyj.biomedcentral.com': 'VirologyJournal',
#     'molecular-cancer.biomedcentral.com': 'MolecularCancer',
#     'plosbiology.org': 'PLOSBiology',
#     'genomemedicine.biomedcentral.com': 'GenomeMedicine',
#     'neuroinflammation.biomedcentral.com': 'Neuroinflammation',
#     'biologydirect.biomedcentral.com': 'BiologyDirect',
#     'bmccellbiol.biomedcentral.com': 'BMCCellBiology',
#     'bmcgenet.biomedcentral.com': 'BMCGenetics',
#     'retrovirology.biomedcentral.com': 'Retrovirology'   # filter3

#    literature
    'fanfiction.net': 'FanFiction',
    'theguardian.com': 'TheGuardian',
    'tvtropes.org': 'TVTropes',
    'archiveofourown.org': 'ArchiveOfOurOwn',
    'doctrinepublishing.com': 'DoctrinePublishing',
    'transcripts.cnn.com': 'CNNTranscripts',
    'everything2.com': 'Everything2',
    'hubpages.com': 'HubPages',
    'reference.com': 'Reference',
    'slate.com': 'Slate',
    'fictionpress.com': 'FictionPress',
    'academyofbards.org': 'AcademyOfBards'

}

# # 转换物理学家和物理名词列表为集合，并转为小写以支持不区分大小写的匹配
# physicist_set = set(physicist.lower() for physicist in physicists)
# term_set = set(term.lower() for term in physics_terms)

# Define read functions
# Define read functions
def read_jsonl_and_filter_by_url(file_path):
    file_path = os.path.join(root_dir, file_path)
    # jsonl_path = os.path.splitext(file_path)[0]  # Remove the extension to get the jsonl file path
    """Read .jsonl.zst or .jsonl file and return parsed JSON objects list"""
    results = []
    total_count = 0
    total_text_length = 0
    # Check if the zst/zstd file exists, otherwise read jsonl file
    # if os.path.exists(file_path):
    # if file_path.endswith('.zst') or file_path.endswith('.zstd'):
    #     with open(file_path, 'rb') as f:
    #         dctx = zstd.ZstdDecompressor()
    #         with dctx.stream_reader(f) as reader:
    #             buffer = b""  # Used to store incomplete lines
    #             while chunk := reader.read(1024):  # Read 1024 bytes at a time
    #                 buffer += chunk
    #                 lines = buffer.split(b"\n")  # Split into lines
    #                 buffer = lines.pop()  # Keep the last part (could be an incomplete line)
    #                 for line in lines:
    #                     if line.strip():  # Skip empty lines
    #                         try:
    #                             results.append(json.loads(line.decode('utf-8')))
    #                         except json.JSONDecodeError as e:
    #                             logging.error(f"Error decoding JSON: {e}")
    #             # Process remaining buffer content
    #             if buffer.strip():
    #                 try:
    #                     results.append(json.loads(buffer.decode('utf-8')))
    #                 except json.JSONDecodeError as e:
    #                     logging.error(f"Error decoding JSON: {e}")
    # elif os.path.exists(jsonl_path):
    # elif file_path.endswith('.jsonl'):
    if file_path.endswith('.jsonl'):
        # If the jsonl file exists, read it line by line
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                # count, text_length = filter_by_url(line, out_dir)
                count, text_length = filter_by_url_and_write(line, out_dir)
                total_count += count
                total_text_length += text_length
                # if line.strip():  # Skip empty lines
                #     try:
                #         results.append(json.loads(line))
                #     except json.JSONDecodeError as e:
                #         logging.error(f"Error decoding JSON: {e}")
    else:
        logging.error(f"File not found: {file_path} ")

    return total_count,total_text_length

# 定义一个字典来管理每个关键词对应的文件信息
file_manager = defaultdict(lambda: {'file': None, 'size': 0, 'index': 0})

# 文件大小限制
MAX_SIZE = 500 * 1024 * 1024  # 500MB
process_start_index =0
process_end_index = 0
def read_filelist(filelist_dir):
    filelist_dir = os.path.abspath(filelist_dir)
    with open(filelist_dir, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file]
    return lines

def open_new_file(keyword, base_dir):
    """根据关键字打开新文件，并更新管理器信息"""
    file_info = file_manager[keyword]
    if file_info['file']:
        file_info['file'].close()
    file_info['index'] += 1
    file_path = os.path.join(base_dir, keyword, f"{process_start_index}-{process_end_index}-{keyword}_{file_info['index']}.jsonl")
    file_info['file'] = open(file_path, 'w', encoding='utf-8')
    portalocker.lock(file_info['file'], portalocker.LOCK_EX)  # 对新文件加锁
    file_info['size'] = 0
    return file_info['file']


def get_file(keyword, base_dir):
    """获取当前可用的文件句柄，若文件超过大小限制，则打开新文件，加锁保证线程安全"""
    file_info = file_manager[keyword]
    if file_info['file'] is None or file_info['size'] > MAX_SIZE:
        if file_info['file'] is not None:
            portalocker.unlock(file_info['file'])  # 解锁旧文件
            file_info['file'].close()
        return open_new_file(keyword, base_dir)
    return file_info['file']

# def write_record(file, record):
#     """写入记录到文件，并更新文件大小"""
#     json_record = json.dumps(record)
#     file.write(json_record + '\n')
#     return len(json_record) + 1

# def filter_by_url(line, base_dir):
#     """根据URL关键字过滤并写入到相应的文件中，返回总记录数和总长度"""
#     count = 0
#     total_length = 0
#     record = json.loads(line)
#     # for record in data:
#     url = record.get('url', '').lower()
#     # matched = False
#
#     # 检查URL中是否包含关键词，并选择对应的文件夹
#     for keyword, folder_name in url_keywords.items():
#         if keyword in url:
#             # 获取当前关键字对应的文件句柄
#             file = get_file(folder_name, base_dir)  # 请确保 get_file 适应了新的需求
#             # 写入记录，并更新文件大小
#             json_record = json.dumps(record)
#             file.write(json_record + '\n')
#             file_manager[folder_name]['size'] += len(json_record) + 1  # 加上换行符的长度
#             # 更新计数和总长度
#             count += 1
#             total_length += len(record.get('text', ''))
#             # matched = True
#             break
#         # if not matched:
#         #     continue  # 如果URL不包含任何已知关键字，则跳过
#
#     return count, total_length

def filter_by_url_and_write(line, base_dir):
    """根据URL关键字过滤并直接写入到相应的文件中，返回总记录数和总长度"""
    count = 0
    total_length = 0

    # 尝试找到"url": 的索引位置
    url_marker = '"url": "'
    start_index = line.find(url_marker)
    if start_index != -1:
        start_index += len(url_marker)  # 调整start_index到URL的开始位置
        end_index = line.find('"', start_index)  # 查找URL结尾的双引号
        if end_index != -1:
            url = line[start_index:end_index].lower()  # 提取并转换为小写的URL
            # 检查URL中是否包含关键词，并选择对应的文件夹
            for keyword, folder_name in url_keywords.items():
                if keyword in url:
                    # 获取当前关键字对应的文件句柄
                    file = get_file(folder_name, base_dir)
                    portalocker.lock(file, portalocker.LOCK_EX)  # 确保文件在写入时加锁
                    file.write(line)  # 直接写入整行数据
                    portalocker.unlock(file)  # 写入完成后解锁
                    file_manager[folder_name]['size'] += len(line) + 1  # 记录增加的文件大小
                    count += 1
                    total_length += len(line)  # 这里使用整行长度作为文本长度
                    break

    return count, total_length

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
# out_dir = "/root/a100_nas_lvbo/peixunban/002754_lvbo/physics_filt"

def main(start_index, end_index, out_dir):
    # 确保关键词文件夹存在
    for folder in url_keywords.values():
        os.makedirs(os.path.join(out_dir, folder), exist_ok=True)
    filelist = get_all_files(root_dir)

    if start_index < 0 or end_index > len(filelist) or start_index > end_index:
        print("Invalid index range")
        return

    selected_files = filelist[start_index:end_index + 1]
    output_file_path = os.path.join(out_dir, f"selected_files_{start_index}_to_{end_index}.txt")
    with open(output_file_path, 'w') as file:
        for path in selected_files:
            file.write(path + '\n')

    total_count = 0
    total_text_length = 0
    total_files = len(selected_files)
    for i, file_path in enumerate(selected_files):
        count, length = read_jsonl_and_filter_by_url(os.path.join(root_dir, file_path))
        # output_file_path = os.path.join(out_dir, f"filtered_file_path{}.jsonl")
        total_count+=count
        total_text_length+=length
        # 计算并打印进度百分比
        progress_percent = ((i + 1) / total_files) * 100
        print(f"Progress: {progress_percent:.2f}% - Processing file {i + 1}/{total_files} (Range: {start_index} to {end_index})")

    write_count_to_file(total_count, total_text_length, out_dir)

    print(f"Processed files from index {start_index} to {end_index}. Found {total_count} relevant texts with a total length of {total_text_length}.")
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
    # start_index = 10000
    # end_index = 10000
    # result = main(start_index, end_index, out_dir)
    process_start_index = start_index
    process_end_index = end_index
    main(start_index, end_index, out_dir)
    # sys.exit(result)
