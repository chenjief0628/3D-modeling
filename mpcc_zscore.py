
#step9.1:  MCC    y:TM-score=0.45的MCC
#puzzle casp15

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import sys

file1_txt = sys.argv[1]    #"casp15_fold_all_zscore_num.txt"
# file2_txt = sys.argv[2]    #"pz_fold_all_zscore_num.txt"



data_x1 = []
data_y1 = []
# data_x2 = []
# data_y2 = []

with open(file1_txt, "r") as file1:
    lines1 = file1.readlines()
for line in lines1[1:]:
    columns = line.split()
    data_x1.append(columns[10])
    data_y1.append(columns[4])

data_x1 = np.array(data_x1).astype(float)
data_y1 = np.array(data_y1).astype(float)
print("min(data_x1), min(data_y1)",min(data_x1), min(data_y1))
print("max(data_x1), max(data_y1)",max(data_x1), max(data_y1))
# print(data_x)
# data_x1 = 1/data_x1
# print(data_x)
# print("++++++++++")
# print(data_y)

# with open(file2_txt, "r") as file2:
#     lines2 = file2.readlines()
# for line in lines2[1:]:
#     columns = line.split()
#     data_x2.append(columns[7])
#     data_y2.append(columns[4])

# data_x2 = np.array(data_x2).astype(float)
# data_y2 = np.array(data_y2).astype(float)
# print("min(data_x2), min(data_y2)",min(data_x2), min(data_y2))
# print("max(data_x2), max(data_y2)",max(data_x2), max(data_y2))
# print(data_x2)
# data_x2 = 1/data_x2
# print(data_x2)
# print("++++++++++")
# print(data_y2)

# def mcc_plot(data_x1,data_y1,data_x2, data_y2,threshold_y):
def mcc_plot(data_x1,data_y1,threshold_y):

    # 创建图表对象
    fig, ax = plt.subplots()
    # 绘制散点图
    # ax.scatter(data_x, data_y)
    # 绘制第一组数据
    ax.scatter(data_x1, data_y1, color='red', marker='o', facecolor='none', edgecolor='red')#, label='casp15'

    # 绘制第二组数据
    # ax.scatter(data_x2, data_y2, color='blue', marker='o', facecolor='none', edgecolor='blue', label='puzzle')
    ax.legend()

    #data_x1,data_x2合并做data_x  mcc
    data_x1=np.array(data_x1)
    # data_x2=np.array(data_x2)
    # print(data_x1)
    # print(data_x2)
    # data_x=np.concatenate([data_x1,data_x2])
    # data_y=np.concatenate([data_y1,data_y2])
    data_x=np.concatenate([data_x1])
    data_y=np.concatenate([data_y1])


    def calculate_mcc(TP, TN, FP, FN):
        TP = float(TP)
        if (TP + FP) * (TP + FN) * (TN + FP) * (TN + FN)==0:
            mcc =0
        else:
            mcc=(TP * TN - FP * FN) / np.sqrt((TP + FP) * (TP + FN) * (TN + FP) * (TN + FN))
        return mcc

    # threshold_y = 0.45
    best_mcc = -1
    best_x = None
    rangx=min(data_x)-0.1
    rangy=max(data_x)+0.1
    step=0.1

    for threshold in np.arange(rangx, rangy, step):  # 根据需要设置阈值范围和步长
        TP = []
        TN = []
        FP = []
        FN = []
    #     print("threshold",threshold)
        for i in range(len(data_x)):
            if data_y[i] > threshold_y:
                if data_x[i] > threshold:
                    TP.append((data_x[i], data_y[i]))
                else:
                    FN.append((data_x[i], data_y[i]))
            else:
                if data_x[i] <= threshold:
                    TN.append((data_x[i], data_y[i]))
                else:
                    FP.append((data_x[i], data_y[i]))

#         print(len(TP), len(TN), len(FP), len(FN))
        mcc = calculate_mcc(len(TP), len(TN), len(FP), len(FN))
    #     print(mcc)

        if mcc > best_mcc:
            best_mcc = mcc
            best_x = threshold


    print(len(data_x))
    # 计算PCC
    pcc = np.corrcoef(data_x, data_y)[0, 1]
#     创建包含 data_x 的 DataFrame
#     df_x = pd.DataFrame({'Column X': data_x})

#     # 创建包含 data_y 的 DataFrame
#     df_y = pd.DataFrame({'Column Y': data_y})

#     # 指定要保存的Excel文件名
#     excel_filename = 'C:/Users/22698/Desktop/meta_score_40/loc_output.xlsx'

#     # 创建一个Excel写入器
#     with pd.ExcelWriter(excel_filename) as writer:
#         df_x.to_excel(writer, sheet_name='Sheet_X', index=False)
#         df_y.to_excel(writer, sheet_name='Sheet_Y', index=False)

    print("PCC:", pcc)
    # 设置 x 轴和 y 轴的上下限
    print("min(score), min(TM-score)",min(data_x),min(data_y))
    print("max(score), max(TM-score)",max(data_x),max(data_y))
    print("PCC:", pcc)
    print("TM-score=",threshold_y)
    print("MAX MCC:", best_mcc)
    print("z(score8):", best_x)
    # print("eRMSD:",1/best_x)
    # min_value = min(min(data_x), min(data_y))
    min_value = rangx-0.2
    # min_value = 0
    # max_value = 1
    # max_value = max(max(data_x)+50, max(data_y)+0.1)
    max_value = rangy+0.2
    ax.set_xlim(min_value, max_value)
    ax.set_ylim(0, 1)
    # 绘制竖线
    plt.axvline(x=best_x, color='k')

    # 绘制横线
    plt.axhline(y=threshold_y, color='k')

    # 添加对角线
    # plt.plot([min_value, max_value], [min_value, max_value], color='red')
    ax.set_xlabel('zscore8')
    ax.set_ylabel('TM-score')
    # 显示图表
    plt.show()

#     warnings.filterwarnings("ignore", category=RuntimeWarning)
#thy_list=[0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.6]
#for thy in thy_list:
#    print("thy",thy)
#    mcc_plot(data_x1,data_y1,data_x2,data_y2,thy)
# mcc_plot(data_x1,data_y1,data_x2, data_y2,0.4)
mcc_plot(data_x1,data_y1,0.4)




