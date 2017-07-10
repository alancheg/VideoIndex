"""
data:2017-7-10
author:alancheg
本程序的主要作用是计算 kmeans 聚类后的数据中心点

输入：需要聚类的内容，聚类的中心点个数
输出：聚类的中心点坐标
"""
import csv
from sklearn.cluster import KMeans
import numpy as np
from time import time

CLUSTER_CENTER = 8


# 数据的格式
# img_name,feature_name,feature_num,cor_x,cor_y
def data_generate(path):
    # 生成标准的位置信息
    data = []
    data_length = 0
    with open(path, "r") as f:
        reader = list(csv.reader(f))
        data_length = len(reader) - 1

        i = 0
        for row in reader[1:]:
            # 去掉首行的标签
            [_, _, _, x, y] = row

            x = int(x)
            y = int(y)

            data.append([x, y])
            i += 1

    return np.asarray(data), data_length


if __name__ == "__main__":

    path = r"C:\Users\alan\Desktop\index_project\data\source.csv"
    data, data_length = data_generate(path)

    start_time = time()
    kmeans = KMeans(n_clusters=CLUSTER_CENTER, random_state=0).fit(data)
    end_time = time()
    print("cluster_time = " + str(end_time - start_time))

    print(kmeans.labels_)
    print(kmeans.cluster_centers_)
