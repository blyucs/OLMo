#!/bin/bash

#tokenizer_model="/root/database/mount/a100_nas/peixunban/002924_lichuan/ocean_score_corpus/ocean_tokenizer_model_1125/tokenizer.json"
tokenizer_model="/home/lvbo/OLMo/olmo_data/tokenizers/allenai_dolma2.json"
#input="/root/database/mount/a100_nas/peixunban/002924_lichuan/ocean_score_corpus/ocean_filter_v2/prob_filter/processed_data/*"
input="/home/lvbo/02_gz_data/Run_20241125-114153_0_to_2000/*.gz"
output="/home/lvbo/test_jlc"

dolma tokens \
    --documents $input \
    --destination $output \
    --tokenizer.name_or_path  $tokenizer_model \
    --tokenizer.eos_token_id 1 \
    --tokenizer.pad_token_id 0 \
    --processes 16 \
    --files_per_process 500 \
    --batch_size 10000 \
    --ring_size 16 \
    --dtype uint16 \
    --seed 1024 \
    #--dryrun \
