# -*- coding:utf-8 -*- #
'''
@author: Leo,bin
'''
import os
import re
import csv

# 存入csv的方法
def csv_writter(datalist, csvfile):
    # 存入csv，将一页评论，拆分成多条，按行存入csv
    b = [datalist[i:i+7] for i in range(0, len(datalist), 7)]

    # 把拆分后的list循环取出，并写入csv的一行
    for data in b:
        spamwriter = csv.writer(csvfile, dialect='excel')
        spamwriter.writerow(data)

def Combine_csvfile(path):
                
    all_data = []
    for i in os.listdir(path):
        if( i == 'error_list.txt'):
            continue
        with open(path+'\\'+i) as csvfile:
            data=csvfile.readlines()
            for j in data:
                all_data.append(re.sub(r'\s+','',j))
    
    
    print(len(all_data))
    
    with open( path + '\\all_data.csv', 'w+') as outfile:
        for i in all_data:
            outfile.write(i+'\n')