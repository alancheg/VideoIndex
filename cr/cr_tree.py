"""
data:2017-7-11
author:alancheg

本文主要对应参考文献中的 cr 树
corner based splitting(cbs) algorithms
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
        def _assign_leaf(leaf, father_node):
            # 将 corner 中的节点分配到父节点中
            father_node.leaves.append(leaf)
            father_node.MBR = merge(father_node.MBR, leaf.MBR)

        def _assign_corner(corner, father_node):
            for leaf in corner:
                father_node.leaves.append(leaf)
                father_node.MBR = merge(father_node.MBR, leaf.MBR)
                leaf.father = father_node

        def _add_min_mbr_node(node1, node2):
            def _mbr_squre(mbr):
                return abs(mbr['xmax'] - mbr['xmin']) * abs(mbr['ymax'] - mbr['ymin'])

            # 将最小的 mbr 合并
            # 将节点 1 中的一个元素分配给 2，并且使得 2 的 MBR 最小
            s = 0
            t = 0

            # 找到 node1 中使得 node2 面积最小的节点，并且记录坐标
            for i in range(len(node1.leaves)):
                if s is 0:
                    s = _mbr_squre(merge(node1.leaves[i].MBR, node2.MBR))
                    t = i
                else:
                    if _mbr_squre(merge(node1.leaves[i].MBR, node2.MBR)) < s:
                        t = i

            # 进行插入操作
            node1.leaves[t].father = node2
            node2.leaves.append(node1.leaves[t])
            node2.MBR = merge(node2.MBR, node1.leaves[t].MBR)
            node1.leaves.pop(t)

        if self.father is None:
            # 父节点的层级比当前节点多1。
            self.father = Rtree(level = self.level + 1, m = self.m, M = self.M)
            self.father.leaves.append(self)

        # 产生新的节点，m、M 和 father 都与当前节点相同。
        Node1 = Rtree(level = self.level, m = self.m, M = self.M, father = self.father)
        Node2 = Rtree(level = self.level, m = self.m, M = self.M, father = self.father)

        # --------------- cbs splitting algo ----------- #
        """
        此算法的核心思想是，
        将节点分配到4个不同的区域，然后选出能够使得区域相对平衡的两个区域
        然后构建出最小矩形
        """
        # # --- cbs v1 start ---- #
        # corner = {}
        # for i in range(1, 4):
        #     corner[i] = []
        #
        # # 通过找到中心点从而将区域分成四个部分
        # (CovRectXcen, CovRectYcen) = (((self.MBR['xmin'] + self.MBR['xmax'])/2),
        #                               ((self.MBR['ymin'] + self.MBR['ymax'])/2))
        #
        # # 将节点分到 4 个区域
        # for node in self.leaves:
        #     (ObjXcen, ObjYcen) = (((node.MBR['xmin'] + node.MBR['xmax'])/2),
        #                           ((node.MBR['ymin'] + node.MBR['ymax'])/2))
        #     if ObjXcen > CovRectXcen:
        #         if ObjYcen > CovRectYcen:
        #             # _assign_leaf(node, Node2)
        #             corner[2].append(node)
        #         else:
        #             corner[3].append(node)
        #     else:
        #         if ObjYcen > CovRectYcen:
        #             # corner1.append(node)
        #             # _assign_leaf(node, Node2)
        #             corner[1].append(node)
        #         else:
        #             # corner0.append(node)
        #             # _assign_leaf(node, Node1)
        #             corner[0].append(node)
        #
        # if abs(len(corner[1])  + len(corner[0]) - len(corner[2]) - len(corner[3])) \
        #         > abs(len(corner[1]) + len(corner[2]) - len(corner[0]) - len(corner[3])):
        #     # 如果左右的数目差值大于上下的，则将节点分为上下
        #     _assign_corner(corner[1], Node1)
        #     _assign_corner(corner[2], Node1)
        #
        #     _assign_corner(corner[3], Node2)
        #     _assign_corner(corner[0], Node2)
        # else:
        #     _assign_corner(corner[1], Node1)
        #     _assign_corner(corner[0], Node1)
        #
        #     _assign_corner(corner[2], Node2)
        #     _assign_corner(corner[3], Node2)
        # # cbs v1 end #

        # 将 4 个区域作为四个节点，试试能否降低时间复杂度

        # # ------ cbs v2 ------ #
        # # 时间仍然不能满足预期 #
        # corner0 = Rtree(level = self.level, m = self.m, M = self.M, father = self.father)
        # corner1 = Rtree(level = self.level, m = self.m, M = self.M, father = self.father)
        # corner2 = Rtree(level = self.level, m = self.m, M = self.M, father = self.father)
        # corner3 = Rtree(level = self.level, m = self.m, M = self.M, father = self.father)
        #
        # # 通过找到中心点从而将区域分成四个部分
        # (CovRectXcen, CovRectYcen) = (((self.MBR['xmin'] + self.MBR['xmax'])/2),
        #                               ((self.MBR['ymin'] + self.MBR['ymax'])/2))
        #
        # # 将节点分到 4 个区域
        # for node in self.leaves:
        #     (ObjXcen, ObjYcen) = (((node.MBR['xmin'] + node.MBR['xmax'])/2),
        #                           ((node.MBR['ymin'] + node.MBR['ymax'])/2))
        #     if ObjXcen > CovRectXcen:
        #         if ObjYcen > CovRectYcen:
        #             # _assign_leaf(node, Node2)
        #             # corner[2].append(node)
        #             corner2.leaves.append(node)
        #             corner2.MBR = merge(corner2.MBR, node.MBR)
        #         else:
        #             # corner[3].append(node)
        #             corner3.leaves.append(node)
        #             corner3.MBR = merge(corner2.MBR, node.MBR)
        #     else:
        #         if ObjYcen > CovRectYcen:
        #             # corner1.append(node)
        #             # _assign_leaf(node, Node2)
        #             # corner[1].append(node)
        #             corner1.leaves.append(node)
        #             corner1.MBR = merge(corner2.MBR, node.MBR)
        #         else:
        #             # corner0.append(node)
        #             # _assign_leaf(node, Node1)
        #             # corner[0].append(node)
        #             corner0.leaves.append(node)
        #             corner0.MBR = merge(corner2.MBR, node.MBR)
        #
        # if abs(len(corner1.leaves)  + len(corner0.leaves) - len(corner2.leaves) - len(corner3.leaves)) \
        #         > abs(len(corner1.leaves) + len(corner2.leaves) - len(corner0.leaves) - len(corner3.leaves)):
        #     # 如果左右的数目差值大于上下的，则将节点分为上下
        #     # _assign_corner(corner[1], Node1)
        #     # _assign_corner(corner[2], Node1)
        #     #
        #     # _assign_corner(corner[3], Node2)
        #     # _assign_corner(corner[0], Node2)
        #     Node1.leaves = corner1.leaves + corner2.leaves
        #     Node1.MBR = merge(corner1.MBR, corner2.MBR)
        #     for leaf in Node1.leaves:
        #         leaf.father = Node1
        #
        #     Node2.leaves = corner3.leaves + corner0.leaves
        #     Node2.MBR = merge(corner3.MBR, corner0.MBR)
        #     for leaf in Node2.leaves:
        #         leaf.father = Node2
        # else:
        #     # _assign_corner(corner[1], Node1)
        #     # _assign_corner(corner[0], Node1)
        #     #
        #     # _assign_corner(corner[2], Node2)
        #     # _assign_corner(corner[3], Node2)
        #     Node1.leaves = corner1.leaves + corner0.leaves
        #     Node1.MBR = merge(corner1.MBR, corner0.MBR)
        #     for leaf in Node1.leaves:
        #         leaf.father = Node1
        #
        #     Node2.leaves = corner2.leaves + corner3.leaves
        #     Node2.MBR = merge(corner3.MBR, corner2.MBR)
        #     for leaf in Node2.leaves:
        #         leaf.father = Node2
        #
        # # cbs v2 end #

        # cbs v3 #
        # corner1 = 0
        # corner2 = 0
        # corner3 = 0
        # corner0 = 0

        corner = {}
        for i in range(4):
            corner[i] = []

        # 通过找到中心点从而将区域分成四个部分
        (CovRectXcen, CovRectYcen) = (((self.MBR['xmin'] + self.MBR['xmax'])/2),
                                      ((self.MBR['ymin'] + self.MBR['ymax'])/2))

        # 将节点分到 4 个区域
        for node in self.leaves:
            (ObjXcen, ObjYcen) = (((node.MBR['xmin'] + node.MBR['xmax'])/2),
                                  ((node.MBR['ymin'] + node.MBR['ymax'])/2))
            if ObjXcen > CovRectXcen:
                if ObjYcen > CovRectYcen:
                    # _assign_leaf(node, Node2)
                    corner[2].append(node)
                    # corner2 += 1
                else:
                    corner[3].append(node)
                    # corner3 += 1
            else:
                if ObjYcen > CovRectYcen:
                    # corner1.append(node)
                    # _assign_leaf(node, Node2)
                    corner[1].append(node)
                    # corner1 += 1
                else:
                    # corner0.append(node)
                    # _assign_leaf(node, Node1)
                    corner[0].append(node)
                    # corner0 += 1

        if abs(len(corner[1]) + len(corner[0]) - len(corner[2]) - len(corner[3])) > abs(len(corner[1]) + len(corner[2]) - len(corner[0]) - len(corner[3])):
            # 如果左右的数目差值大于上下的，则将节点分为上下
            # _assign_corner(corner[1], Node1)
            # _assign_corner(corner[2], Node1)
            # _assign_corner(corner[3], Node2)
            # _assign_corner(corner[0], Node2)
            Node1.leaves = corner[1] + corner[2]
            for leaf in Node1.leaves:
                Node1.MBR = merge(Node1.MBR, leaf.MBR)
                leaf.father = Node1

            Node2.leaves = corner[3] + corner[0]
            for leaf in Node2.leaves:
                Node2.MBR = merge(Node2.MBR, leaf.MBR)
                leaf.father = Node2

        else:
            Node1.leaves = corner[1] + corner[0]
            for leaf in Node1.leaves:
                Node1.MBR = merge(Node1.MBR, leaf.MBR)
                leaf.father = Node1

            Node2.leaves = corner[3] + corner[2]
            for leaf in Node2.leaves:
                Node2.MBR = merge(Node2.MBR, leaf.MBR)
                leaf.father = Node2

        while(len(Node1.leaves) < Node1.m):
            _add_min_mbr_node(Node2, Node1)

        while (len(Node2.leaves) < Node1.m):
            _add_min_mbr_node(Node1, Node2)

                # _assign_corner(corner[1], Node1)
            # _assign_corner(corner[0], Node1)
            #
            # _assign_corner(corner[2], Node2)
            # _assign_corner(corner[3], Node2)

        # cbs v3 end #

        # # 将节点分配到不同的区域
        # for node in self.leaves:
        #     (ObjXcen, ObjYcen) = (((node.MBR['xmin'] + node.MBR['xmax'])/2),
        #                           ((node.MBR['ymin'] + node.MBR['ymax'])/2))
        #
        #     if ObjXcen > CovRectXcen:
        #         if ObjYcen > CovRectYcen:
        #             _assign_leaf(node, Node2)
        #         else:
        #             _assign_leaf(node, Node1)
        #     else:
        #         if ObjYcen > CovRectYcen:
        #             # corner1.append(node)
        #             _assign_leaf(node, Node2)
        #         else:
        #             # corner0.append(node)
        #             _assign_leaf(node, Node1)

        # while(len(Node1.leaves) < Node1.m):
        #     _add_min_mbr_node(Node2, Node1)
        #
        # while(len(Node2.leaves) < Node2.m):
        #     _add_min_mbr_node(Node1, Node2)

        # -------- cbs end ----------------- #

        self.father.leaves.remove(self)
        self.father.leaves.append(Node1)
        self.father.leaves.append(Node2)
        self.father.MBR = merge(self.father.MBR, Node1.MBR)
        self.father.MBR = merge(self.father.MBR, Node2.MBR)

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


    # Search搜索给定的矩形范围。
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


    # FindLeaf查找给定的对象。
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


    # CondenseTree对树进行压缩。
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


    # CondenseRoot用来对根节点进行压缩。
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
