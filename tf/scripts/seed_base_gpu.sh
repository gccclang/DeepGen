#!/usr/bin/env bash

#!/bin/bash

# Data
DATA_ROOT=../data/seed/

# Model
DIV_VAL=1
N_LAYER=12
D_MODEL=512
D_EMBED=512
N_HEAD=10
D_HEAD=500
D_INNER=1024

# Training
TGT_LEN=80
MEM_LEN=250


BSZ=32
NUM_CORE=4

TEST_TGT_LEN=80
TEST_MEM_LEN=250
TEST_CLAMP_LEN=200

#TEST_BSZ=10
TEST_BSZ=1

TEST_NUM_CORE=1


if [[ $1 == 'train_data' ]]; then
    python data_utils.py \
        --data_dir=${DATA_ROOT}/ \
        --dataset=seed \
        --tgt_len=${TGT_LEN} \
        --per_host_train_bsz=${BSZ} \
        --per_host_valid_bsz=${BSZ} \
        --num_passes=1 \
        --use_tpu=False \
        ${@:2}
elif [[ $1 == 'test_data' ]]; then
    python data_utils.py \
        --data_dir=${DATA_ROOT}/ \
        --dataset=seed \
        --tgt_len=${TEST_TGT_LEN} \
        --per_host_test_bsz=${TEST_BSZ} \
        --num_passes=1 \
        --use_tpu=False \
        ${@:2}
elif [[ $1 == 'train' ]]; then
    echo 'Run training...'
    CUDA_VISIBLE_DEVICES='0' python3.6 train_gpu.py \
        --data_dir=${DATA_ROOT}/tfrecords \
        --record_info_dir=${DATA_ROOT}/tfrecords/ \
        --corpus_info_path=${DATA_ROOT}/corpus-info.json \
        --model_dir=EXP-seed4-1_head-1e4 \
        --div_val=${DIV_VAL} \
        --untie_r=True \
        --proj_share_all_but_first=True \
        --n_layer=${N_LAYER} \
        --d_model=${D_MODEL} \
        --d_embed=${D_EMBED} \
        --n_head=${N_HEAD} \
        --d_head=${D_HEAD} \
        --d_inner=${D_INNER} \
        --dropout=0.1 \
        --dropatt=0.0 \
        --learning_rate=0.00010 \
        --warmup_steps=0 \
        --train_steps=14000 \
        --tgt_len=${TGT_LEN} \
        --mem_len=${MEM_LEN} \
        --train_batch_size=${BSZ} \
        --num_core_per_host=${NUM_CORE} \
        --iterations=100 \
        --save_steps=1000 \
        ${@:2}
elif [[ $1 == 'eval' ]]; then
    echo 'Run evaluation...'
    CUDA_VISIBLE_DEVICES='1' python3.6 train_gpu.py \
        --data_dir=${DATA_ROOT}/tfrecords \
        --record_info_dir=${DATA_ROOT}/tfrecords/ \
        --corpus_info_path=${DATA_ROOT}/corpus-info.json \
        --model_dir=EXP-wt103 \
        --div_val=${DIV_VAL} \
        --untie_r=True \
        --proj_share_all_but_first=True \
        --n_layer=${N_LAYER} \
        --d_model=${D_MODEL} \
        --d_embed=${D_EMBED} \
        --n_head=${N_HEAD} \
        --d_head=${D_HEAD} \
        --d_inner=${D_INNER} \
        --dropout=0.1 \
        --dropatt=0.0 \
        --tgt_len=${TGT_LEN} \
        --mem_len=${MEM_LEN} \
        --clamp_len=${CLAMP_LEN} \
        --same_length=True \
        --eval_batch_size=${BSZ} \
        --num_core_per_host=${NUM_CORE} \
        --do_train=False \
        --do_eval=True \
        --eval_split=test \
        ${@:2}
elif [[ $1 == 'inference' ]]; then
    echo 'Run inference...'
    CUDA_VISIBLE_DEVICES='1' python3.6 train_gpu.py \
        --data_dir=${DATA_ROOT}/tfrecords \
        --record_info_dir=${DATA_ROOT}/tfrecords/ \
        --corpus_info_path=${DATA_ROOT}/corpus-info.json \
        --model_dir=EXP-seed4-1_head-1e4 \
        --div_val=${DIV_VAL} \
        --untie_r=True \
        --proj_share_all_but_first=True \
        --n_layer=${N_LAYER} \
        --d_model=${D_MODEL} \
        --d_embed=${D_EMBED} \
        --n_head=${N_HEAD} \
        --d_head=${D_HEAD} \
        --d_inner=${D_INNER} \
        --dropout=0.0 \
        --dropatt=0.0 \
        --tgt_len=${TGT_LEN} \
        --mem_len=${MEM_LEN} \
        --clamp_len=${TEST_CLAMP_LEN} \
        --same_length=True \
        --eval_batch_size=${BSZ} \
        --num_core_per_host=${TEST_NUM_CORE} \
        --do_train=False \
        --do_inference=True \
        --eval_split=test \
        ${@:2}


else
    echo 'unknown argment 1'
fi
