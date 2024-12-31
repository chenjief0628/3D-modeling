Because the file 202210b_pdb is larger than the upload size for GitHub, I used the split command on 202210b_pdb.tar.gz to split it. The command is:

bash
split -b 100M 202210b_pdb.tar.gz 202210b_lib_
The split files are 202210b_lib_aa, 202210b_lib_ab, and 202210b_lib_ac.

Before extracting, I need to restore the files:

bash
cat 202210b_lib_aa > 202210b_pdb.tar.gz
cat 202210b_lib_ab >> 202210b_pdb.tar.gz
cat 202210b_lib_ac >> 202210b_pdb.tar.gz
Then, extract the file using:

bash
tar xzvf 202210b_pdb.tar.gz

