import csv
import os
import glob
import io
import pandas as pd
import re
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

#     csv_path = os.path.join(csv_directory, filename + ".csv")
    
    try:
        with open(csv_path, 'r') as file:
            print(f"Opened file: {filename}")
            jnum = csv_dir[-1]
            csv_reader = csv.reader(file)  
            lines = []

            for line in csv_reader:
                if line[0].startswith("; ALIGN "):
                    lines.append(line)

            # print(lines[4:])
            # 打印结果
            data_dict = {}

            for sublist in lines[4:]:
                for line in sublist:
                    value = line.split()

                    if len(value) >= 3:
                        key = value[2]
                        value = line[36:].strip()

                        if key in data_dict:
                            data_dict[key].append(value)
                        else:
                            data_dict[key] = [value]

            # print(data_dict)
            result = []
            pos = []
            templet = []
            first_key = list(data_dict.keys())[0]
            second_key = list(data_dict.keys())[1]
            third_key = list(data_dict.keys())[2]
            first_value = data_dict[first_key][1:-1]
            second_value = data_dict[second_key][1:-1]
            third_value = data_dict[third_key]
            first_value = ', '.join(first_value).replace(' ', '').replace(',', '')
            second_value = ', '.join(second_value).replace(' ', '').replace(',', '')
            third_value = ', '.join(third_value).replace(' ', '').replace(',', '')
            first_pos_value = data_dict[first_key][0]  
            last_pos_value = data_dict[first_key][-1]  
            second_pos_value = data_dict[second_key][0]  
            slast_pos_value = data_dict[second_key][-1]  
            result.extend([first_value, second_value, third_value, first_pos_value, last_pos_value, second_pos_value, slast_pos_value])

            for item in result[3:]:
                item = item.strip("Begin ").strip("End ")  
                pos.append(item)

            for item1 in result[:3]:
                item1 = item1.replace(" ", "") 
                templet.append(item1)
            big1=int(pos[0])
            big2=int(pos[2])
            atom_lines=[]
            filename=filename+".pdb"
            temp_path = os.path.join(temp_pdb_path, filename)
            with open(temp_path, 'r', encoding='UTF-8') as pdb_file:
                for line in pdb_file:
                    atom_lines.append(line)
            atom_new_lines=[]
            flag1 = 0
            flag2 = 0
            for i, (item1, item2) in enumerate(zip(templet[0], templet[1])):
                index1=i+big1
                index2=i+big2
                if item1=="-":
                    flag1=flag1+1
                elif item2=="-":
                    flag2=flag2+1
                else:
                    for atom_line in atom_lines:
                        #print("i  flag   i-flag   atom_line[22:26]",i, flag, i-flag, int(atom_line[22:26]))
                        if index2-flag2 == int(atom_line[22:26]):
                            col_22_26 = str(index1-flag1)
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

