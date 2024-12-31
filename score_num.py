###
import pandas as pd
import numpy as np
import sys

#####python score_num.py score example_output/fold_score

def score_num(input_txt, save_txt):
    df = pd.read_csv(input_txt, sep='\s+', header=None, names=['Col1', 'Col2', 'Col3'])
    df['Col4'] = df.groupby('Col1')['Col3'].rank(method='first', ascending=False).astype(int)

    #print("Updated DataFrame:")
    print(df)
    grouped = df.groupby('Col1').size().reset_index(name='Count')
    print(grouped)
    df.to_csv(save_txt, sep='\t', index=False, header=False)
    print(save_txt)

def zscore_num(input_txt, save_txt):
    df = pd.read_csv(input_txt, sep='\t', header=None, names=['Col1', 'Col2', 'Col3', 'Col4', 'Col5'])

    df['Col6'] = df.groupby('Col1')['Col5'].rank(method='first', ascending=False).astype(int)

    print("Updated DataFrame:")
    print(df)
    df.to_csv(save_txt, sep='\t', index=False, header=False)
    print(save_txt)

def soft_meta_score_num(input_txt, save_txt):
    df = pd.read_csv(input_txt, sep='\s+', header=None, names=['Col1', 'Col2', 'Col3', 'Col4', 'Col5', 'Col6', 'Col7'])

    df['Col8'] = df.groupby('Col1')['Col7'].rank(method='first', ascending=False).astype(int)

    print("Updated DataFrame:")
    print(df)
    df.to_csv(save_txt, sep='\t', index=False, header=False)
    print(save_txt)

def meta_score_num(input_txt, save_txt):
    df = pd.read_csv(input_txt, sep='\s+', header=None, names=['Col1', 'Col2', 'Col3', 'Col4', 'Col5', 'Col6', 'Col7', 'Col8', 'Col9'])

    df['Col10'] = df.groupby('Col1')['Col7'].rank(method='first', ascending=False).astype(int)

    print("Updated DataFrame:")
    print(df)
    df.to_csv(save_txt, sep='\t', index=False, header=False)
    print(save_txt)

if __name__ == "__main__":
    type=sys.argv[1]
    input_file=sys.argv[2]      
    input_txt=input_file+".txt"
    save_txt=input_file+"_num.txt"
    if type == "score":
        score_num(input_txt, save_txt)
    elif type == "soft_meta":
        soft_meta_score_num(input_txt, save_txt)
    elif type == "meta":
        meta_score_num(input_txt, save_txt)

