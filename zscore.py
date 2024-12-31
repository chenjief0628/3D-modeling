###根据自身score的归一化值，选择top1/top5 best/top5 aver,计算tmscore平均值
import pandas as pd
import numpy as np
import sys
from score_num import zscore_num
#
input_file=sys.argv[1]
file_txt = input_file+".txt" 
nor_txt=input_file+"_zscore.txt"
nor_num_txt=input_file+"_zscore_num.txt"
print(file_txt)
print(nor_txt)
print(nor_num_txt)
def cal_zscore(file_txt, nor_txt):
    data = np.genfromtxt(file_txt, delimiter='\t', usecols=2)
    # print(data)
    # data = np.concatenate((data1))

    print(len(data))
    mean_val = np.mean(data)
    std_val = np.std(data,ddof=1)

    print("Mean:", mean_val)
    print("Standard Deviation:", std_val)

    new_lines=[]
    with open(file_txt, "r") as file:
        lines = file.readlines()
        for line in lines:
            columns = line.split()
            zscore=(float(columns[2])-mean_val)/std_val
            columns.append(zscore)
            new_lines.append(columns[0]+"\t"+columns[1]+"\t"+columns[2]+"\t"+columns[3]+"\t"+str(zscore))
            # print(new_lines)
            # new_lines=np.array(new_lines)
    with open(nor_txt, 'w') as file:
        for line in new_lines:
            file.write(line)
            file.write("\n")



cal_zscore(file_txt, nor_txt)
zscore_num(nor_txt, nor_num_txt)

