def remove_empty_lines(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as input_file:
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for line in input_file:
                if line.strip():  # 检查行是否不为空（不仅仅是空白字符）
                    output_file.write(line)  # 写入非空行到新文件

# 调用函数，输入你的文件路径
input_path = '/workspace/lvbo_a100/peixunban/002754_lvbo/physics_filt/NCBI_1.jsonl'
output_path = '/workspace/lvbo_a100/peixunban/002754_lvbo/physics_filt/NCBI_1.json'

remove_empty_lines(input_path, output_path)
