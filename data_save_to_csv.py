# 本文件的主要作用就是将数据集进行抽取并且存储为对应表结构的 csv 文件。#
import csv
import pymysql
import xml.dom.minidom
import os

data_path = './data/'


def connet_database():
    conn = pymysql.connect(host="192.168.254.129", port=3306, user="alan", passwd="alan", db="mit_image",
                           charset="utf8")
    cur = conn.cursor()
    return conn, cur


def xml_parser(file_path, cursor, conn):
    # 打开xml文档
    dom = xml.dom.minidom.parse(file_path)

    # 得到文档元素对象
    root = dom.documentElement

    file_name = dom.getElementsByTagName('filename')[0].firstChild.data
    # print(file_name[0].firstChild.data)

    object_list = dom.getElementsByTagName('object')

    count = 0
    for object in object_list:
        name = object.getElementsByTagName('name')[0].firstChild.data
        # print(name)
        # print('num:', count)

        polygon = object.getElementsByTagName('polygon')[0]
        point_list = polygon.getElementsByTagName('pt')

        for point in point_list:
            point_x = point.getElementsByTagName('x')[0].firstChild.data
            point_y = point.getElementsByTagName('y')[0].firstChild.data

            insert_data = (
            str(file_name).replace('\n', ''), str(name).replace('\n', ''), count, int(str(point_x).replace('\n', '')),
            int(str(point_y).replace('\n', '')))
            sql = 'insert into feature(img_name, feature_name, feature_num, cordinate_x, cordinate_y) values' + str(
                insert_data)

            cursor.execute(sql)
        # print(sql)

        count = count + 1

    conn.commit()


def xml_parser_to_csv(file_path, csv_writer):
    # 此程序的主要作用是将 xml 文件进行解析，并且输出到 csv 文档
    # 同时， csv 文件中的行号将作为类似于数据库的主键， 唯一区分所有数据。

    # 打开xml文档
    dom = xml.dom.minidom.parse(file_path)

    # 得到文档元素对象
    root = dom.documentElement

    file_name = dom.getElementsByTagName('filename')[0].firstChild.data
    # print(file_name[0].firstChild.data)

    object_list = dom.getElementsByTagName('object')

    count = 0
    for object in object_list:

        name = object.getElementsByTagName('name')[0].firstChild.data
        # print(name)
        # print('num:', count)

        polygon = object.getElementsByTagName('polygon')[0]
        point_list = polygon.getElementsByTagName('pt')

        for point in point_list:
            point_x = point.getElementsByTagName('x')[0].firstChild.data
            point_y = point.getElementsByTagName('y')[0].firstChild.data

            insert_data = [str(file_name).replace('\n', ''), str(name).replace('\n', ''), count,
                           int(str(point_x).replace('\n', '')), int(str(point_y).replace('\n', ''))]
            csv_writer.writerow(insert_data)

        count = count + 1


if __name__ == "__main__":

    # ----------------------- data to csv --------------------- #
    # 循环遍历文件夹中的数据，然后调用 xml 解析器进行数据库写入

    with open(os.path.join(data_path, 'source.csv'), 'a+', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # 先写入各项名称
        csv_writer.writerow(['img_name', 'feature_name', 'feature_num', 'cor_x', 'cor_y'])

        s = os.sep  # 根据unix或win，s为\或/
        root_path = r'D:\video_process\MIT Image Dataset\Annotations\Anno_XML'

        # 将根目录中的所有文件名读入列表中
        file_name_list = []
        for root, dirs, files in os.walk(root_path):
            # print("Root = ", root, "dirs = ", dirs, "files = ", files)
            file_name_list = files

        # print(file_name_list)

        for file_name in file_name_list:
            file_path = os.path.join(root_path, file_name)

            # print(file_path)
            xml_parser_to_csv(file_path, csv_writer)

            # ----------------------- data to mysql ----------------- #
            # # 连接数据库
            # conn, cursor = connet_database()
            #
            # # 循环遍历文件夹中的数据，然后调用 xml 解析器进行数据库写入
            #
            # s = os.sep #根据unix或win，s为\或/
            # root_path = r'D:\MIT Image Dataset\Annotations\Anno_XML'
            #
            # # 将根目录中的所有文件名读入列表中
            # file_name_list = []
            # for root, dirs, files in os.walk(root_path):
            # 	# print("Root = ", root, "dirs = ", dirs, "files = ", files)
            # 	file_name_list = files
            # # print(file_name_list)
            #
            # for file_name in file_name_list:
            # 	file_path = os.path.join(root_path, file_name)
            # 	print(file_path)
            # 	xml_parser(file_path, cursor, conn)
            #
            # conn.close()
