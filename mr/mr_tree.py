"""
data:2017-7-10
author:alancheg

本文件基于已有的 R 树算法，主要改进了相关的节点分裂算法
"""
#!/usr/bin/python
# -*- coding: utf-8 -*-
#定义存储的对象，包含其位置信息MBR，level固定为0表明在底层，index为其在数据库中的索引，father为其父节点。
import random
from math import sqrt

class node(object):
    def __init__(self, MBR = None, level = 0, index = None, father = None):
        if(MBR == None):
            self.MBR = {'xmin':None, 'xmax':None, 'ymin':None, 'ymax':None}
        else:
            self.MBR = MBR
        self.level = level
        self.index = index
        self.father = father


# MBR 最小边界矩形
# 定义R树的节点，包含其位置信息MBR，level为其层数，默认为1为叶子节点，m和M为其子节点数的最小和最大值，father为其父节点。
class Rtree(object):

    def __init__(self, leaves = None, MBR = None, level = 1, m = 1, M = 3, father = None):
        self.leaves = []
        if(MBR == None):
            self.MBR = {'xmin':None, 'xmax':None, 'ymin':None, 'ymax':None}
        else:
            self.MBR = MBR
        self.level = level
        self.m = m
        self.M = M
        self.father = father

    # ChooseLeaf选择插入的节点。
    def ChooseLeaf(self, node):
        # 如果当前节点的层数比要插入的节点高1层，表明找到了合适的节点。
        if self.level == node.level + 1:
            return self
        else:
            # 否则对其子节点的MBR遍历，找到面积增加的最小值。
            increment = [(i, space_increase(self.leaves[i].MBR, node.MBR)) for i in range(len(self.leaves))]
            res = min(increment, key = lambda x:x[1])
            return self.leaves[res[0]].ChooseLeaf(node)

    # SplitNode 分裂节点。
    def SplitNode(self):
        """
        在分裂的过程中，如果当前的节点没有父节点，那么需要产生新的节点，否则不需要
        如果当前节点有父节点，则生成两个新的节点替换当前的节点
        """
        # def FindMassCorner(NodeList):
        #     """
        #     查找质心的函数，通过在每一次分裂中选择质心点作为主要节点，从而增强算法的效率。
        #     :param NodeList:
        #     :return:MassNode1, MassNode2
        #     """
        #     mass_node = random.sample(NodeList, 2)
        #
        #     for item in
        #
        #     return MassNode1, MassNode2

        # 如果当前节点没有父节点，则必然需要产生父节点来容纳分裂的两个节点。
        # def leaf_distance(center, leaf):
        #     return ((leaf.MBR['xmin'] - center.MBR['xmin']) ** 2 + (leaf.MBR['ymin'] - center.MBR['ymin']) ** 2) ** 0.5

        def leaf_distance(center, leaf):
            # 距离度量函数 v2 ，通过将距离换乘面积来减少时间复杂度
            return abs((leaf.MBR['xmin'] - center.MBR['xmin']) * (leaf.MBR['ymin'] - center.MBR['ymin']))

        def calc_mass_center(center, node):
            # 增加点之后计算质心，返回新的质心
            pass

        if self.father is None:
            # 父节点的层级比当前节点多1。
            self.father = Rtree(level = self.level + 1, m = self.m, M = self.M)
            self.father.leaves.append(self)

        # 产生新的节点，m、M 和 father 都与当前节点相同。
        leaf1 = Rtree(level = self.level, m = self.m, M = self.M, father = self.father)
        leaf2 = Rtree(level = self.level, m = self.m, M = self.M, father = self.father)

        # 调用PickSeeds为leaf1和leaf2分配子节点
        # self.PickSeeds(leaf1, leaf2)

        # # ---------------  todo： 矩阵法 暂时不适用 ------------------------- #
        # # 构建一个距离矩阵，减少计算量
        # # 构建的矩阵为一个上三角矩阵，
        # # i = j 时 为 0 i < j 时为 -1
        # # ---- 构建两个特殊的矩阵，从而减少时间复杂度 ---------#
        # nearest_father = []
        # distance_matrix = []
        #
        #
        # for num_1 in range(len(self.leaves)):
        #     now_list = []
        #     for num_2 in range(len(self.leaves)):
        #         if num_1 == num_2:
        #             now_list.append(0)
        #         elif num_1 > num_2:
        #             now_list.append(leaf_distance(self.leaves[num_1], self.leaves[num_2]))
        #         else:
        #             now_list.append(-1)
        #
        # i = 0
        # j = 0
        #
        # sum_distance = 0
        # # 中心点判断函数，找出能够使得总体中心点距离最小的函数
        # for i in range(len(self.leaves)):
        #     for j in range(i+1, len(self.leaves)):
        #         pass
        #
        # # ----------- end ---------- #


        # # 遍历剩余的子节点，进行插入。
        # while len(self.leaves) > 0:
        #     # 如果剩余的子节点插入某一组才能使该组节点数大于m，则直接全部插入进去，并调整MBR。
        #     if len(leaf1.leaves) > len(leaf2.leaves) and len(leaf2.leaves) + len(self.leaves) == self.m:
        #         for leaf in self.leaves:
        #             leaf2.MBR = merge(leaf2.MBR, leaf.MBR)
        #             leaf2.leaves.append(leaf)
        #             leaf.father = leaf2
        #         self.leaves = []
        #         break
        #
        #     if len(leaf2.leaves) > len(leaf1.leaves) and len(leaf1.leaves) + len(self.leaves) == self.m:
        #         for leaf in self.leaves:
        #             leaf1.MBR = merge(leaf1.MBR, leaf.MBR)
        #             leaf1.leaves.append(leaf)
        #             leaf.father = leaf1
        #         self.leaves = []
        #         break
        #
        #     # 否则调用PickNext为leaf1和leaf2分配下一个节点。
        #     # self.PickNext(leaf1, leaf2)

        # 当前节点的父节点删除掉当前节点并加入新的两个节点，完成分裂。

        # todo: 质心法，测试有效性 #
        # 1. 随机找到两个初始的质心点
        mass_center1 = random.randint(0,int(len(self.leaves)/2))
        mass_center2 = random.randint(int(len(self.leaves)/2), len(self.leaves))

        # 2. 求出使得距离最小的数据项
        # choose_node = -1
        node_list_1 = []
        node_list_2 = []



        # ---- end ------- #

        self.father.leaves.remove(self)
        self.father.leaves.append(leaf1)
        self.father.leaves.append(leaf2)
        self.father.MBR = merge(self.father.MBR, leaf1.MBR)
        self.father.MBR = merge(self.father.MBR, leaf2.MBR)

    # # PickSeeds为两组节点分配子节点。
    # # todo:增加质心属性，从而提高 R 树的分裂效率
    # def PickSeeds(self, leaf1, leaf2):
    #     """
    #     MR 树
    #     此版本的改进是通过引入质心的属性来提高整个 R 树的节点分裂效率
    #
    #     """
    #     # todo: 如何简化距离度量函数
    #     # 减少平方和立方的数量应该可以提高算法的速度
    #
    #     # def leaf_distance(center, leaf):
    #     #     # 距离度量函数 v1 ，多次的平方和开根号容易导致时间增加
    #     #     return ((leaf.MBR['xmin'] - center.MBR['xmin']) ** 2 + (leaf.MBR['ymin'] - center.MBR['ymin']) ** 2) ** 0.5
    #
    #     def leaf_distance(center, leaf):
    #         # 距离度量函数 v2 ，通过将距离换乘面积来减少时间复杂度
    #         return abs((leaf.MBR['xmin'] - center.MBR['xmin']) * (leaf.MBR['ymin'] - center.MBR['ymin']))
    #
    #     d = 0
    #     t1 = 0
    #     t2 = 0
    #
    #     # # 遍历所有可能的子节点组合，寻找差值最大的项。
    #     # for i in range(len(self.leaves)):
    #     #     for j in range(i + 1, len(self.leaves)):
    #     #         # -------------------------------------------------------- #
    #     #         MBR_new = merge(self.leaves[i].MBR, self.leaves[j].MBR) # 合并两个 MBR
    #     #         S_new = 1.0 * (MBR_new['xmax'] - MBR_new['xmin']) * (MBR_new['ymax'] - MBR_new['ymin'])
    #     #
    #     #         S1 = 1.0 * (self.leaves[i].MBR['xmax'] - self.leaves[i].MBR['xmin']) * (self.leaves[i].MBR['ymax'] - self.leaves[i].MBR['ymin'])
    #     #         S2 = 1.0 * (self.leaves[j].MBR['xmax'] - self.leaves[j].MBR['xmin']) * (self.leaves[j].MBR['ymax'] - self.leaves[j].MBR['ymin'])
    #     #
    #     #         if S_new - S1 - S2 > d:
    #     #             t1 = i
    #     #             t2 = j
    #     #             d = S_new - S1 - S2
    #     #         # -------------------------------------------------------- #
    #
    #     # 计算出最小距离点
    #     # 通过随机指定两个值，计算点的距离和，找出能够使总体距离和最小的值
    #     for i in range(len(self.leaves)):
    #         for j in range(i+1, len(self.leaves)):
    #
    #             sum_of_distance = 0
    #             for k in range(len(self.leaves)):
    #                 if k is not i and k is not j:
    #                     sum_of_distance += min(leaf_distance(self.leaves[i], self.leaves[k]), leaf_distance(self.leaves[j], self.leaves[k]))
    #
    #             if sum_of_distance > d:
    #                 d = sum_of_distance
    #                 t1 = i
    #                 t2 = j
    #
    #     # --------- 新的方法 ------------- #
    #     # 找出数据中的质心，从而确定中心点
    #     # data_list = []
    #     #
    #     #
    #     # distance = 0
    #     # addr = []
    #     # for i in range(data_list):
    #     #     for j in range(data_list):
    #     #         pass
    #
    #     # --------- end ----------------- #
    #
    #     n2 = self.leaves.pop(t2)
    #     n2.father = leaf1
    #     leaf1.leaves.append(n2)
    #     leaf1.MBR = leaf1.leaves[0].MBR
    #
    #     n1 = self.leaves.pop(t1)
    #     n1.father = leaf2
    #     leaf2.leaves.append(n1)
    #     leaf2.MBR = leaf2.leaves[0].MBR
    #
    # # PickNext为两组节点分配一个子节点。
    # def PickNext(self, leaf1, leaf2):
    #     # 距离计算函数
    #     def leaf_distance(center, leaf):
    #         return ((leaf.MBR['xmin'] - center.MBR['xmin']) ** 2 + (leaf.MBR['ymin'] - center.MBR['ymin']) ** 2) ** 0.5
    #
    #     # # ------------------- old way -------- #
    #     # d = 0
    #     # t = 0
    #     #
    #     # # 遍历子节点，找到插入两组节点后面积增加差值最大的一项。
    #     # for i in range(len(self.leaves)):
    #     #     d1 = space_increase(merge(leaf1.MBR, self.leaves[i].MBR), leaf1.MBR)
    #     #     d2 = space_increase(merge(leaf2.MBR, self.leaves[i].MBR), leaf2.MBR)
    #     #     if abs(d1 - d2) > abs(d):
    #     #         d = d1 - d2
    #     #         t = i
    #     #
    #     # if d > 0:
    #     #     target = self.leaves.pop(t)
    #     #     leaf2.MBR = merge(leaf2.MBR, target.MBR)
    #     #     target.father = leaf2
    #     #     leaf2.leaves.append(target)
    #     # else:
    #     #     target = self.leaves.pop(t)
    #     #     leaf1.MBR = merge(leaf1.MBR, target.MBR)
    #     #     target.father = leaf1
    #     #     leaf1.leaves.append(target)
    #     # # ------------------ old way end --------- #
    #
    #     # 传统的方法是找出使得面积最大的子节点
    #     # 新的方法是找出使得节点更加紧密的子节点
    #     # ------------------- new way ------------ #
    #     d = 0
    #     t = 0
    #
    #     # 找到一个子节点，分配给一个离它最近的面积
    #     if leaf_distance(leaf2, self.leaves[t]) > leaf_distance(leaf1, self.leaves[t]):
    #         d = 1
    #
    #     if d > 0:
    #         target = self.leaves.pop(t)
    #         leaf2.MBR = merge(leaf2.MBR, target.MBR)
    #         target.father = leaf2
    #         leaf2.leaves.append(target)
    #     else:
    #         target = self.leaves.pop(t)
    #         leaf1.MBR = merge(leaf1.MBR, target.MBR)
    #         target.father = leaf1
    #         leaf1.leaves.append(target)
    #     # ------------------- new way end --------- #


    # AdjustTree自底向上调整R树。
    def AdjustTree(self):
        p = self
        while p != None:
            #如果当前节点的叶子数量超过M，则分裂并调整父节点的MBR。
            if len(p.leaves) > p.M:
                p.SplitNode()
            else:
                #否则调整父节点的MBR。
                if p.father != None:
                    p.father.MBR = merge(p.father.MBR, p.MBR)
            p = p.father


#Search搜索给定的矩形范围。
    def Search(self, MBR):
        result = []
        #如果已经到达叶子节点，则在result中直接添加对象。
        if self.level == 1:
            for leaf in self.leaves:
                if intersect(MBR, leaf.MBR):
                    result.append(leaf.index)
            return result
        #否则对与目标MBR相交的子节点进行Search，并与result相加。
        else:
            for leaf in self.leaves:
                if intersect(MBR, leaf.MBR):
                    result = result + leaf.Search(MBR)
            return result


#FindLeaf查找给定的对象。
    def FindLeaf(self, node):
        result = []
        #如果当前节点不是叶子节点，则递归寻找所有包含目标MBR的子节点。
        if self.level != 1:
            for leaf in self.leaves:
                if contain(leaf.MBR, node.MBR):
                    result.append(leaf.FindLeaf(node))
            for x in result:
                if x != None:
                    return x
        #若当前结点是叶子节点，则直接遍历这些对象，判断index是否相等，并返回。
        else:
            for leaf in self.leaves:
                if leaf.index == node.index:
                    return self


#CondenseTree对树进行压缩。
    def CondenseTree(self):
        #Q用来保存要插入的节点。
        Q = []
        p = self
        q = self
        while p != None:
            p.MBR = {'xmin':None, 'xmax':None, 'ymin':None, 'ymax':None}
            #重新路径上的MBR
            for leaf in p.leaves:
                p.MBR = merge(p.MBR, leaf.MBR)
            #如果当前节点的叶子树小于m，则其父节点中删除该节点，如果该节点仍然含有子节点，则子节点需要重新插入。
            if len(p.leaves) < self.m and p.father != None:
                p.father.leaves.remove(p)
                if len(p.leaves) != 0:
                    Q = Q + p.leaves
            q = p
            p = p.father
        #重新插入要插入的节点
        for node in Q:
            q = Insert(q, node)


#CondenseRoot用来对根节点进行压缩。
    def CondenseRoot(self):
        p = self
        q = p
        #如果根节点只有一个子节点，则替换子节点为根节点，直到根节点为叶子节点或根节点有多个子节点。
        while len(p.leaves) == 1 and p.father == None and p.level != 1:
            p = p.leaves[0]
            q.leaves = []
            p.father = None
            q = p
        return p

#Insert插入新节点，返回更新后的根节点。
def Insert(root, node):
    target = root.ChooseLeaf(node)
    node.father = target
    target.leaves.append(node)
    target.MBR = merge(target.MBR, node.MBR)
    target.AdjustTree()
    if root.father != None:
        root = root.father
    return root

#Delete删除目标对象，返回更新后的根节点。
def Delete(root, node):
    target = root.FindLeaf(node)
    if target == None:
        # print 'no result'
        print("no result")
        return root
    target.leaves.remove(node)
    target.CondenseTree()
    root = root.CondenseRoot()
    return root

#merge用来合并两个MBR。
def merge(MBR1, MBR2):
    if MBR1['xmin'] == None:
        return MBR2
    if MBR2['xmin'] == None:
        return MBR1
    MBR = {}
    MBR['xmin'] = min(MBR1['xmin'], MBR2['xmin'])
    MBR['ymin'] = min(MBR1['ymin'], MBR2['ymin'])
    MBR['xmax'] = max(MBR1['xmax'], MBR2['xmax'])
    MBR['ymax'] = max(MBR1['ymax'], MBR2['ymax'])
    return MBR

#space_increase用来计算MBR2合并到MBR1之后MBR1的面积增加。
def space_increase(MBR1, MBR2):
    xmin = min(MBR1['xmin'], MBR2['xmin'])
    ymin = min(MBR1['ymin'], MBR2['ymin'])
    xmax = max(MBR1['xmax'], MBR2['xmax'])
    ymax = max(MBR1['ymax'], MBR2['ymax'])
    return 1.0 * ((xmax - xmin) * (ymax - ymin) - (MBR1['xmax'] - MBR1['xmin']) * (MBR1['ymax'] - MBR1['ymin']))

#intersect判断MBR1和MBR2是否有交集。
def intersect(MBR1, MBR2):
    if MBR1['xmin'] > MBR2['xmax'] or MBR1['xmax'] < MBR2['xmin'] or MBR1['ymin'] > MBR2['ymax'] or MBR1['ymax'] < MBR2['ymin']:
        return 0
    return 1

#contain判断MBR1是否包含MBR2。
def contain(MBR1, MBR2):
    return (MBR1['xmax'] >= MBR2['xmax'] and MBR1['xmin'] <= MBR2['xmin'] and MBR1['ymax'] >= MBR2['ymax'] and MBR1['ymin'] <= MBR2['ymin'])
