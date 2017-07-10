"""
B+ 树索引
本程序的主要运行逻辑：
    1. 对数据进行树状索引的构建
    2. 将索引文件进行存储

之后的查询文件会将索引加载到内存中

在测试的过程中，通过使用文件名作为主键进行测试
"""
import csv
import os
import time
import bisect


# b_class = 10  #在本次试验中，构建的是 10 阶 b+ 树
CONST_MAX_KEY = 10
CONST_MAX_KEY = 5


class BtreeNode:
    """
    节点需要几个主要的特点，
    首先，节点需要有对应值的地址，父节点的地址，子节点的地址
    TODO: 如何对一个节点的子节点进行排序（）


    """
    def __init__(self):
        """
        key 指定了相应的数据地址，如果 key 值为 0 ,说明不是叶子节点，反之为叶子节点
        parrent 存储了当前节点的父节点地址，默认为 None
        child 存储了当前节点的子节点地址 使用 字典结构方便结构，同时 child 应该保证
              其 child.key 的数目 小于最大子节点数目
        """

        self.key = []
        self.parrent = None
        self.child = {}

    # def add_key(self, key):
    #     """
    #     :param key:
    #     :return:
    #     -----------------------
    #     函数功能： 添加关键词
    #     此部分主要的实现逻辑是：
    #     1. 给定关键词
    #     2. 查找关键词的位置
    #     3. 在给定的位置插入关键词（插入关键词造成的各种反应不在此函数中实现）
    #
    #     """
    #     pos = self.find_sub_position(key)
    #     self.keys.insert(pos, key)
    #     self.children.insert(pos + 1, None)
    #     return pos
    #
    # def del_key(self):
    #     pass
    #
    # def find_sub_position(self):
    #     pass
    #
    # def find_key_positon(self):
    #     pass
    #
    # def find_children_position(self):
    #     pass
    #
    # def has_children(self):
    #     pass
    #
    # def split(self):
    #     """
    #
    #     :return:
    #
    #     ---------------------------
    #     此函数是重点，节点的分裂有几种情况
    #     """
    #     pass


class BplusTree:
    """
    具体的实现，初步的设想是以文件名作为关键词（后期的改进中将会实现指定关键词的索引。）
    在初步检索的过程中，通过文件名遍历实现检索

    在没有指针的情况下如何存储树？需要方便树结构的修改。
    为了方便树结构的修改，在每一个树中，需要存储相关父节点的信息。

    将字典的 key 作为地址，同时子节点存储相关的 key 用于检索，同时也方便节点的插入时
    能够很快的进行构建，当所有的节点构建完成之后，建立一张列表作为整个索引。

    在每一次的构建中，都需要刷新索引文件。
    """

    """
    一个非叶节点需要包含的信息  [父节点，索引值，子节点1-n]
    一个叶节点需要包含的信息 [父节点，元素的地址]
    
    """
    def __init__(self, keynum, parent):
        """
        :param keynum:
        :param parent:

        ----------------------------------------
        对存储的结构进行规范化
        tree_dict 的结构 key:[[父节点key],[子节点1,...,子节点n],[值1， 。。。 值n]]
        index_list 是根据 tree_dict 进行生成的。
        """
        self.root = BtreeNode
        self.tree_dict = {}
        self.index_list = []
        self.count_num = 0  ## 用于记录节点个数, 从 0 开始

    def find_position(self, key):
        """
        :param key:
        :return:
        -----------------------
        本函数的功能是，给定数据，找到节点应该插入的位置
        """
        if len(self.root.child.keys()) == 0:
            # 当 root 节点为空时
            # node =
            pass

        return pos

    def insert_node(self, element):
        """
        :param node:     # 默认将元素的关键词存储在元素列表的首位
        :return:None

        将新的节点插入之后有几种状况
        1. 新插入的节点不影响树的结构
        2. 新插入的节点印象了树的结构
            2.1 插入的节点影响了 b+ 树的规则，导致了节点的分裂
            2.2 插入的节点影响了 父节点的 值，从而需要对父节点的值进行修改
        """
        def find_position():
            """

            :return:
            -------------------

            """


            return pos

        key = element[0]

        if self.count_num == 1:
            # 此时节点为根节点
            self.tree_dict.append('1', [])
            self.tree_dict[1].append([0])
            self.tree_dict[1].append([])
            # self.tree_dict[1].


    def _delete_node(self, element):
        pass

    def find_node(self, key):\
        pass


# class DataStruct:
#     """
#     本类的主要作用是将数据进行基本的结构化。
#     通过对数据的基本结构化，实现数据库中索引使用的基本功能
#     """
#     def __init__(self, list):
#         if len(list) > 0:
#             primary_key = list(0)  # 默认将第一个元素设置为主键，用于检索
#         item_list = list[1:len(list)]  # 除了主键之外的其他元素不参与索引过程


def key_compare(key1, key2):
    # 本函数主要的功能是对比不同键的大小，从而进行构建
    # 在此次实现中,只需要进行基本的对比就行
    if key1 >= key2:
        return key1
    else:
        return key2


def build_b_plus_tree_index(input_path="./data/source.csv"):
    # 通过调用树的函数实现基本的索引构建
    with open(input_path) as f:
        reader = csv.reader(f)
        for row in reader:
            # 将每行数据进行插入
            pass


def test_index():
    # 测试索引的性能
    pass


if __name__ == '__main__':
    pass

