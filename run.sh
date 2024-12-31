#!/bin/bash


fasta_lib="202210b_fasta_noT_len_lib"       # Template FASTA *.fasta
lib_ids="202210b_id_30.txt"    #"202210b_lib_id.txt"  # IDs for the template FASTA
pdb_lib="202210b_pdb_noT_len_lib"   # Template PDB *.pdb

fasta_dir="example"  # Folder containing the target .fasta files
output_dir="example_output"  ## Path for the output files

fold_path="/data/liuz/software/foldalign.2.5.3/bin/foldalign"
lara_path="/data/liuz/software/lara/lara"
loc_path="locarna"  
rnamo_path="/data/liuz/software/RNAmountAlign-1.0/src/RNAmountAlign"

output_meta_pdb="${output_dir}/output_meta_pdb"
mkdir -p "${output_meta_pdb}"
meta_score="${output_dir}/meta_zscore"
if [ -f "${meta_score}" ]; then
    rm "${meta_score}"
fi
top=10
meta_score_top="${meta_score}_top${top}.txt"
soft_list=(fold loc lara rnamo)
for soft in "${soft_list[@]}"; do
    echo "================= ${soft} ================" 
    soft_path_var="${soft}_path"
    soft_path=$(eval echo \$$soft_path_var)
    echo "$soft_path"

    output_csv="${output_dir}/output_${soft}"
    mkdir -p "${output_csv}"
    ### csv
    ./${soft}_align.sh "${fasta_lib}" "${lib_ids}" "${fasta_dir}" "${output_csv}" "${soft_path}"

    # ### score
    score_file="${output_dir}/${soft}_score"
    ./score_${soft}.sh "${output_csv}" "${score_file}.txt"
    python score_num.py score "${score_file}"

    # # ### pdb
    output_pdb="${output_dir}/output_${soft}_pdb"
    mkdir -p "${output_pdb}"
    python ${soft}_pdb.py "${pdb_lib}" "${output_csv}" "${score_file}_num.txt" "${output_pdb}"

    # ###zscore 
    python zscore.py "${score_file}_num"


    # ### meta 8
    zscore_txt="${score_file}_num_zscore_num.txt"
    mpcc_path=mpcc_zscore.csv   
    soft_meta="${output_dir}/${soft}_meta_zscore"

    grep "$soft" "$mpcc_path"
    mcc=$(awk -v pattern="$soft" '$0 ~ pattern {print $3}' "$mpcc_path")
    zscore0=$(awk -v pattern="$soft" '$0 ~ pattern {print $4}' "$mpcc_path")
    pcc=$(awk -v pattern="$soft" '$0 ~ pattern {print $5}' "$mpcc_path")
    echo $mcc
    echo $zscore0
    echo $pcc
    awk -v x="$zscore0" -v y="$pcc" '{ $7 = ($5 - x) / x * y; print }' "$zscore_txt" > "${soft_meta}.txt"
    echo "${soft_meta}.txt finish!"

    python score_num.py soft_meta "${soft_meta}" 

    awk -v soft="$soft" '{print $0, soft}' "${soft_meta}_num.txt" >> "${meta_score}.txt"
done

python score_num.py meta "${meta_score}" 
### top pdb
awk -v num="$top" '$10 <= num { print }' "${meta_score}_num.txt" | sort -k10,10n >"${meta_score_top}"

./meta_pdb.sh "${meta_score_top}" "${output_dir}" "${output_meta_pdb}"
