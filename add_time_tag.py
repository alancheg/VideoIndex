"""
@date: 2017-7-13
@author: alancheg

本程序主要的作用是为2 维的数据集添加时间属性，从而进行时空数据的试验
"""
import csv
import time

if __name__ == "__main__":

    with open('./data/source.csv', 'r') as read_file:
        with open('./source_with_time.csv', 'w') as write_file:
            reader = list(csv.reader(read_file))
