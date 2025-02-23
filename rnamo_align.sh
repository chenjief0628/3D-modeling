#!/bin/bash

fasta_lib=$1
lib_path=$2
fasta_dir=$3
output_folder=$4
soft_path=$5   #"/data/liuz/software/RNAmountAlign-1.0/src/RNAmountAlign"

for fasta_file1 in "$fasta_dir"/*.fasta; do
    filename1=$(basename -- "${fasta_file1%.fasta}")
    echo $filename1
    
    echo $lib_path
    echo "-------rnamount---------"
    while IFS= read -r line; do
        lib_id=$(echo "$line" | awk '{print $1}'| cut -d'.' -f1)
        echo "$lib_id"

        fasta_id_path="$fasta_lib/$lib_id.fasta"
        echo $fasta_id_path
        # IFS='\t' read -ra fasta_paths <<< "$fasta_id_path"
        fasta_paths=($fasta_id_path)

        for fasta_file2 in "${fasta_paths[@]}"; do
            if [ -f "$fasta_file2" ]; then 
                echo $fasta_file2 
                filename2=$(basename -- "${fasta_file2%.fasta}")
                echo "$filename2"

                fasta_length=$(awk 'NR==2{print length($0)}' "$fasta_file2")

                if [ "$fasta_length" -lt 300 ]; then
		            line1=$(sed -n '2p' "$fasta_file1")
		            line2=$(sed -n '2p' "$fasta_file2")
                    align_output=$($soft_path -s "$line1" "$line2")

                    # if [[ $align_output =~ "No structural alignment was found." ]]; then
                    #     echo "No structural alignment was found between $filename1 and $filename2."
                    # else 
                    output_dir="$output_folder/$filename1"
                    [ ! -d "$output_dir" ] && mkdir -p "$output_dir"
                     
                    output_filename="$output_dir/$filename2.csv"
                    echo "$align_output" > "$output_filename"
                    echo "Alignment saved to $output_filename"
                    # fi
                else
                    echo "Skipping foldalign for $filename2: Second line length is greater than or equal to 500."
                fi
            else
                echo "$fasta_file2 file does not exist"
            fi
        done
    done < $lib_path
done

