#zhangtian
import ast
import csv
import os
import glob
import io
import pandas as pd
import re
from collections import OrderedDict
import numpy as np
import traceback
import sys

temp_pdb_path=sys.argv[1]
csv_dir=sys.argv[2]
score_sort_file=sys.argv[3]
out_pdb_path=sys.argv[4]

with open(score_sort_file, 'r') as file:
    lines = file.readlines()

for line in lines[1:]:  
    col=line.strip().split('\t')
    pdbid=col[0]
    filename=col[1]
    num=col[3]
    csv_path=csv_dir+"/"+pdbid+"/"+filename+".csv"
    print("csv_path",csv_path)
    pdbid_lower = pdbid.lower()

    print(pdbid_lower)
# for filename in listdir:
#     csv_path = os.path.join(csv_directory, filename+".csv")

    #     try:
    with open(csv_path, 'r') as file:
        print(f"Opened file: {filename}")
    #         jnum = csv_dir[-1]
        csv_reader = csv.reader(file)  
        lines = []
        for line in csv_reader:
#            if len(line) > 0 and (str(line[0]).startswith(pdbid_lower) or str(line[0]).startswith(filename)):
            if len(line) > 0 and  str(line[0]).startswith(filename):
                lines.append(prev_line)
                lines.append(line)
            prev_line = line
#    print(lines)
    result_dict = {}
    for row in lines:
#        print(row)
        key = row[0].split()[0]  
        value = row[0].split()[1] 
        if key not in result_dict:
            result_dict[key] = [] 
        result_dict[key].append(value) 
    result_dict = {k: ''.join(v) for k, v in result_dict.items()}
    relist= list(result_dict.values())
    # print(relist)
    sequence1=relist[0]
    sequence2=relist[1]
    filename=filename+".pdb"
    temp_path = os.path.join(temp_pdb_path, filename)
    #print(temp_path)
    atom_lines=[]
    with open(temp_path, 'r', encoding='UTF-8') as pdb_file:
        for line in pdb_file:
            atom_lines.append(line)
        atom_new_lines=[]
        flag1 = 0
        flag2 = 0
        for i, (item1, item2) in enumerate(zip(sequence1, sequence2)):
            i=i+1
            if item1=="-":
                flag1=flag1+1
            elif item2=="-":
                flag2=flag2+1
            else:
                
                for atom_line in atom_lines:
                    #print("i  flag   i-flag   atom_line[22:26]",i, flag, i-flag, int(atom_line[22:26]))
                    if i-flag2 == int(atom_line[22:26]):
                        col_22_26 = str(i-flag1)
                        col_22_26_formatted = "{:>4}".format(col_22_26)  
                        atom_new_line= atom_line[:19] + item1 +atom_line[20:22]+ col_22_26_formatted + atom_line[26:]
                        atom_new_lines.append(atom_new_line)
        #print(atom_new_lines)

    out_pdb_directory = out_pdb_path+"/"+pdbid
    if not os.path.exists(out_pdb_directory):
        os.makedirs(out_pdb_directory)
    output_path = os.path.join(out_pdb_directory,pdbid+"_"+str(num)+"_"+filename)
    with open(output_path, 'w') as output_file:
        for line in atom_new_lines:
            output_file.write(line.rstrip() + '\n') 

