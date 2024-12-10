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

TIME=$(date "+%Y_%m_%d_%H_%M_%S")
export TASK_NAME=olmo1b_$TIME 
echo "task name: ${TASK_NAME}"
export WANDB_API_KEY=74c39c7f810caa79a4b9b7d97b918047d8ba6457

#export INPUT_PATH="/mnt/zhongziban/peixunban/002754_lvbo/ocean_token_corpus/"
#export OUTPUT_PATH="/mnt/zhongziban/peixunban/002754_lvbo/llm_models/"
export INPUT_PATH="/mnt/zhongziban/peixunban/002754_lvbo"
export OUTPUT_PATH="/mnt/zhongziban/peixunban/002754_lvbo/save_check"

export load_path="${OUTPUT_PATH}/olmo1b_2024_12_06_04_04_24/latest-unsharded"

#export NUM_GPU=$( lspci | grep -i nvidia | wc -l )
echo "before CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES}"
export CUDA_VISIBLE_DEVICES="0,1,2,3,4,5,6,7"
#export CUDA_VISIBLE_DEVICES="0,1"
export NUM_GPU=8
#export NUM_GPU=2
export config_path="configs/official/OLMo-1B-tiny-macrobatch-2.yaml"
echo "NUM_GPU=${NUM_GPU}"
echo "PYTHONPATH=$PYTHONPATH"
echo "config_path=$config_path"

echo "Checking PyTorch version..."
torch_version=$(python -c "import torch; print(torch.__version__)")
echo "PyTorch version: $torch_version"

#watch -n 2 "nvidia-smi >> ${OUTPUT_PATH}/logs/${TASK_NAME}.txt" &
nohup watch -n 60 "nvidia-smi >> ${OUTPUT_PATH}/logs/${TASK_NAME}.txt" &

PYTHONPATH="./":$PYTHONPATH \
torchrun --nproc_per_node=${NUM_GPU} scripts/train.py \
    ${config_path} \
    --run_name=$TASK_NAME \
    --input_path=${INPUT_PATH} \
    --output_path=${OUTPUT_PATH} \
    --wandb.project=llm-class \
    --wandb.name=$TASK_NAME  \
    2>&1 | tee ${OUTPUT_PATH}/logs/${TASK_NAME}.log