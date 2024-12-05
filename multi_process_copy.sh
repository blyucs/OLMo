#!/bin/bash
export OMP_NUM_THREADS=1

# Define the path to the Python script
SCRIPT_PATH="append_files_and_filt_quality.py"

# Define current project directory
cur_project_dir="$(pwd)"
echo "Current project path: $cur_project_dir"

# Define script directory
cur_script_dir="$(dirname "$(realpath "$0")")"
echo "Script path: $cur_script_dir"

# Navigate to the project directory
cd "$cur_project_dir"
echo "Changed to directory: $(pwd)"

# 定义基地址
base_dir="/root/a100_nas_lvbo/peixunban/002754_lvbo/physics_filt"

# Total number of files and range
START_FILE=${1:-27000}    # Default to 0 if not specified
END_FILE=${2:-27500}    # Default to 199 if not specified
# Number of cores to use
NUM_CORES=${3:-20}
# 创建一个以当前日期和时间命名的文件夹
current_time=$(date "+%Y%m%d-%H%M%S")
folder_name="Run_${current_time}_${START_FILE}_to_${END_FILE}"
out_dir="${base_dir}/${folder_name}"
mkdir -p $out_dir

# Calculate total number of files to process
TOTAL_FILES=$((END_FILE - START_FILE + 1))


# Number of files each core should process
FILES_PER_CORE=$((TOTAL_FILES / NUM_CORES))

# Check if the Python script exists
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "Error: Python script not found at $SCRIPT_PATH"
    exit 1
fi

# Empty wikipedia_counts.txt to store new statistics
#> "$out_dir/wikipedia_counts.txt"

# Execute Python script to process specified file range
for ((i=0; i<NUM_CORES; i++)); do
    start_index=$((START_FILE + i * FILES_PER_CORE))
    end_index=$((start_index + FILES_PER_CORE - 1))

    # Adjust the last batch to ensure all files are processed
    if [ $i -eq $((NUM_CORES - 1)) ]; then
        end_index=$END_FILE
    fi

    echo "Processing files from $start_index to $end_index"
    python3 "$SCRIPT_PATH" $start_index $end_index $out_dir &  # Run in background
done

## Wait for all background jobs to finish
#wait
#
## Summarize results
#total_count=0
#total_text_length=0
#while IFS=',' read -r count text_length; do
#    total_count=$((total_count + count))
#    total_text_length=$((total_text_length + text_length))
#done < "$out_dir/wikipedia_counts.txt"
#echo "Total filtered entries from all files: $total_count"
## Convert bytes to gigabytes
#gigabytes=$(echo "$total_text_length / 1073741824" | bc -l)
## Format output to three decimal places
#formatted_gigabytes=$(printf "%.3f GB" $gigabytes)
#echo "Total text length: $formatted_gigabytes"
