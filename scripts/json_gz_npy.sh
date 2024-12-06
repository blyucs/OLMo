#!/bin/bash
# 切换到脚本应当执行的目录
cd /home/lvbo/OLMo || exit
export PYTHONPATH=./
# 输入 JSON 目录列表
declare -a json_dirs=(
#    "/home/lvbo/DCLM-data/Run_20241125-114153_0_to_2000/"
#    "/home/lvbo/DCLM-data/Run_20241125-114925_2000_to_4000/"
#    "/home/lvbo/DCLM-data/Run_20241125-223437_4000_to_6000/"
#    "/root/lvbo/002754_lvbo/00_DCLM_DATA/Run_20241125-223448_6000_to_8000"
#    "/root/lvbo/002754_lvbo/00_DCLM_DATA/Run_20241125-225207_10000_to_12000"
#    "/root/lvbo/002754_lvbo/00_DCLM_DATA/Run_20241125-225347_12000_to_14000"
#    "/root/lvbo/002754_lvbo/00_DCLM_DATA/Run_20241126-091826_14000_to_16000"
#    "/root/lvbo/002754_lvbo/00_DCLM_DATA/Run_20241126-091852_16000_to_18000"
#    "/root/lvbo/002754_lvbo/00_DCLM_DATA/Run_20241127-090807_18000_to_20000"
#    "/root/lvbo/002754_lvbo/00_DCLM_DATA/Run_20241127-090831_20000_to_22000"
#    "/root/lvbo/002754_lvbo/00_DCLM_DATA/Run_20241127-090852_22000_to_24000"
#    "/root/a100_nas_lvbo/peixunban/002754_lvbo/physics_filt/26000-27000_ALL"
#    "/root/a100_nas_lvbo/peixunban/002754_lvbo/physics_filt/Run_20241205-213909_27000_to_27500"
    "/root/lvbo/002754_lvbo/00_DCLM_DATA/Run_20241127-090947_24000_to_26000"
)
QUALITY_THRES=0.04
# 单一的 GZ 输出目录和 NPY 输出目录
GZ_DIR="/home/lvbo/04_gz_all_common"
NPY_DIR="/root/a100_nas_lvbo/peixunban/002754_lvbo/17_npy_gpt_uint16_24000_26000_$QUALITY_THRES"

# 最大 GZ 文件大小设置
MAX_SIZE_GB=5

# 函数来处理每组路径
process_group() {
    local json_dir=$1
    local index=$2
    local gz_subdir="$GZ_DIR/$(basename $json_dir)"
    local npy_subdir="$NPY_DIR/$(basename $json_dir)"

    echo "处理第 $index 组路径从 $json_dir..."
    echo "开始将 JSON 文件打包成 GZ 格式到 $gz_subdir..."
    python scripts/jsongz.py "$json_dir" "$GZ_DIR" --max_size_gb $MAX_SIZE_GB --quality_thres $QUALITY_THRES

    echo "JSON 到 GZ 的转换完成。开始转换 GZ 到 NPY 格式到 $npy_subdir..."
    python scripts/prepare_memmap_dataset.py "$gz_subdir" -o "$NPY_DIR"

    echo "第 $index 组数据处理完成。"
}

# 循环处理每组路径并行执行
for (( i=0; i<${#json_dirs[@]}; i++ )); do
    process_group "${json_dirs[i]}" $((i+1)) &
done

# 等待所有后台任务完成
wait

# 清空 GZ_DIR 目录中的所有文件
echo "清空 GZ 目录..."
rm -rf "$GZ_DIR"/*

echo "所有数据处理流程已完成。"