#!/bin/bash

meta_score_top=$1
pdb_dir=$2
output_meta_pdb=$3

while IFS= read -r line; do
    pdb_id=$(echo "$line" | cut -d$'\t' -f1)
    temp_id=$(echo "$line" | cut -d$'\t' -f2)
    soft_num=$(echo "$line" | cut -d$'\t' -f4)
    soft=$(echo "$line" | cut -d$'\t' -f9)
    meta_num=$(echo "$line" | cut -d$'\t' -f10)
    echo "$pdb_id"

    pdb1="${pdb_dir}/output_${soft}_pdb/${pdb_id}/${pdb_id}_${soft_num}_${temp_id}.pdb"
    pdb2="${output_meta_pdb}/${pdb_id}_${meta_num}_${temp_id}.pdb"
    echo "$pdb1"
    echo "$pdb2"
    if [ -f "$pdb1" ]; then
        echo "$output_meta_pdb"
        cp "$pdb1" "$pdb2"
    fi
done < "$meta_score_top"

