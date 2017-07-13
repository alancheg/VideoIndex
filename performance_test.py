"""
@date: 2017-7-11
@author: alancheg

this code is used to test the performance of each tree
"""
from time import time
import random


def performance_test(tree_root, search_range, test_num):
    """
    test the avg time of search in the tree
    ----------------------------
    :param tree_root: the root of tree
    :param search_range: the range of the test dataset
    :return: the average time of search
    """
    time_list = []

    data_list = []
    for i in range(test_num):
        data_list.append([random.randint(0, search_range[0]), random.randint(0, search_range[1])])

    # 搜索的输入应该是一个 MBR

    for i in range(len(data_list)):
        MBR = {'xmin':data_list[i][0], 'xmax':data_list[i][0] + 0.1,
               'ymin':data_list[i][1], 'ymax':data_list[i][1] + 0.1}

        start_time = time()
        result = tree_root.Search(MBR)
        end_time = time()

        time_list.append(end_time - start_time)

        node_num = len(result)
        print(node_num)

    return sum(time_list)/len(time_list)


if __name__ == "__main__":
    performance_test()