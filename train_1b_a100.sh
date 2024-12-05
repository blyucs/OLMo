#/bin/bash

nvidia-smi

nvcc --version

export script_path=$(dirname "$0")
echo "script_path=${script_path}"
export code_path="${script_path}"
echo "code_path=${code_path}"
# cd code_path
cd $code_path
pwd
echo "current workpath: ${code_path}"

TIME=$(date "+%Y-%m-%d_%H-%M")
export TASK_NAME=olmo1b_$TIME 
echo "task name: ${TASK_NAME}"
#export WANDB_API_KEY=42cc6f11eac6a0e2d0c218044917b6f8e1189831

#export INPUT_PATH="/mnt/zhongziban/peixunban/002754_lvbo/ocean_token_corpus/"
#export OUTPUT_PATH="/mnt/zhongziban/peixunban/002754_lvbo/llm_models/"
export INPUT_PATH="/root/a100_nas_lvbo/peixunban/002754_lvbo/"
export OUTPUT_PATH="/root/a100_nas_lvbo/peixunban/002754_lvbo/save_check/"

#export load_path="${OUTPUT_PATH}/olmo1b_2024-12-03_10-08/step78000-unsharded/"

#export NUM_GPU=$( lspci | grep -i nvidia | wc -l )
echo "before CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES}"
#export CUDA_VISIBLE_DEVICES="0,1,2,3,4,5,6,7"
export CUDA_VISIBLE_DEVICES="0,1"
export NUM_GPU=2
export config_path="configs/official/OLMo-1B-tiny.yaml"
echo "NUM_GPU=${NUM_GPU}"
echo "PYTHONPATH=$PYTHONPATH"
echo "config_path=$config_path"

PYTHONPATH="./":$PYTHONPATH \
torchrun --nproc_per_node=${NUM_GPU} scripts/train.py \
    ${config_path} \
    --run_name=$TASK_NAME \
    --input_path=${INPUT_PATH} \
    --output_path=${OUTPUT_PATH} \
    --wandb.project=llm-class \
    --wandb.name=$TASK_NAME  \
#    --load_path=$load_path \
    > ${OUTPUT_PATH}/logs/${TASK_NAME}.log 2>&1
