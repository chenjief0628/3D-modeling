import csv
import os
import glob
import io
import pandas as pd
from collections import OrderedDict
import ast
import sys
import traceback

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
# for filename in listdir:
#     csv_path = os.path.join(csv_directory, filename+".csv")
    try:
        with open(csv_path, 'r') as file:
            print(f"Opened file: {filename}")
            jnum = csv_dir[-1]
            csv_reader = csv.reader(file)  
            next(csv_reader)
            rseq = next(csv_reader)
            tseq = next(csv_reader)
            seq_list = []
            seq_list.append(rseq)
            seq_list.append(tseq)
            #print(seq_list)
        filename=filename+".pdb"
        temp_path = os.path.join(temp_pdb_path, filename)
        #print(temp_path)
        l1=[]
        l2=[]
        flatten_data = [element for sublist in seq_list for element in sublist]
        atom_lines=[]
        with open(temp_path, 'r', encoding='UTF-8') as pdb_file:
            for line in pdb_file:
                atom_lines.append(line)
        atom_new_lines=[]
        flag1 = 0
        flag2 = 0
        for i, (item1, item2) in enumerate(zip(flatten_data[0], flatten_data[1])):
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

        out_pdb_directory = out_pdb_path+"/"+pdbid
        if not os.path.exists(out_pdb_directory):
            os.makedirs(out_pdb_directory)
        output_path = os.path.join(out_pdb_directory,pdbid+"_"+str(num)+"_"+filename)
        with open(output_path, 'w') as output_file:
            for line in atom_new_lines:
                output_file.write(line.rstrip() + '\n')  
    except Exception as e:
        print(f"Error processing file: {filename}")
        print(f"Error message: {str(e)}")
        continue
