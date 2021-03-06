#!/usr/bin/python
# -*- coding: utf-8 -*-
from cr_and_mr.mr_tree import *
from random import uniform
from time import time
import csv
from performance_test import performance_test


# 数据的格式
# img_name,feature_name,feature_num,cor_x,cor_y
def data_generate(path, length=200001):
    # 生成标准的位置信息
    data = {}
    data_length = 0
    with open(path, "r") as f:
        reader = list(csv.reader(f))[:length]
        data_length = len(reader) - 1

        i = 0
        for row in reader[1:]:
            # 去掉首行的标签
            [_, _, _, x, y] = row

            x = float(x)
            y = float(y)

            data[i] = {'xmin':x, 'xmax':x + 0.01, 'ymin':y, 'ymax':y + 0.01}
            i += 1

    return data, data_length

if __name__ == "__main__":
    # data = {}
    # #初始化10000个坐标在(-1000, 1000)间，面积为0.01的矩形。
    # for i in range(100000):
    #     x = uniform(-1000, 1000)
    #     y = uniform(-1000, 1000)
    #     data[i] = {'xmin':x, 'xmax':x + 0.01, 'ymin':y, 'ymax':y + 0.01}
    csv_path = r"C:\Users\alan\Desktop\index_project\data\source.csv"
    data, data_length = data_generate(csv_path)

    # for k in range(1, 100):
    #设置一个根节点，m=3，M=7
    k = 20
    root = Rtree(m=k, M=2*k + 1)
    n = []

    for i in range(data_length):
        n.append(node(MBR = data[i], index = i))
    t0 = time()
    print("数据加载完成，总共 " + str(data_length) + " 条数据" )

    # ------------- 插入节点 -------------------------- #
    print("开始构建索引")
    for i in range(data_length):
        root = Insert(root, n[i])
    t1 = time()
    # print ('Inserting ...')
    print ("索引构建完成，总共有 " + str(data_length) + " 条数据，耗时：")
    print (t1 - t0)

    # # ------------- 搜索节点 --------------------------- #
    # time_search_start = time()
    # x = root.Search(merge(n[0].MBR, n[1].MBR))
    # time_search_end = time()
    # # print ('Searching ...')
    # print("检索完成，耗时 :")
    # print (time_search_end - time_search_start)

    # --------- use performance_test get the avg search time ---- #
    print(k)
    print(" mr 树 中 100 条随机检索的平均用时为：")
    print(performance_test(root, [800, 800], 100))

    # -------------- 节点删除 -------------------------- #
    # for i in range(100000):
    #     root = Delete(root, n[i])
    # t3 = time()
    # print ('Deleting ...')
    # print (t3 - t2)
