#!/bin/bash

input_dir=$1 
score_txt=$2  

if [[ -f $score_txt ]]; then
	rm $score_txt
fi
for dir in $input_dir/*; do
	echo $dir
	if [[ -d $dir ]]; then
		#echo $dir
		pdb_id=$(basename $dir)
		#echo $pdb_id
		for file in $dir/*csv; do
			echo $file
			file_name=$(basename $file .${file##*.})
			# echo $file_name
			score=$(grep -o "score .*" $file | awk '{gsub("\\)", "", $2); print $2}')
			echo $score
			echo -e "$pdb_id\t$file_name\t$score"
			echo -e "$pdb_id\t$file_name\t$score" >> $score_txt
		done
	fi
done	


