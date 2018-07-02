import matplotlib.pyplot as plt
import random as rd
import math


def variable(width, height, density, cluster_density):
    """variables"""
    node_member, cluster_member, station, shot_dis_data = [], [], [], []
    len_nodes = math.ceil(density * (width * height))
    len_cluster = math.ceil(cluster_density * len_nodes)

    return node_member, cluster_member, station, shot_dis_data, len_nodes, len_cluster


def base_station(num_base, station):
    """input base station point"""
    for item in range(num_base):
        station.append(map(int, "51,-1".split(',')))
    # split 2d list to 1d list
    base_x, base_y = zip(*station)
    return station, base_x, base_y


def random_node(node_member, len_nodes, width, height, station):
    """random Node"""
    count = 0
    while len(node_member) != len_nodes:
        random_x, random_y = rd.randint(0, width), rd.randint(0, height)
        if [random_x, random_y] not in node_member and \
                [random_x, random_y] not in station:
            node_member.append([random_x, random_y])
        count += 1
    # split 2d list to 1d list
    node_x, node_y = zip(*node_member)
    return node_member, node_x, node_y


def random_cluster(cluster_member, len_cluster, node_member):
    """random Cluster from amount Node"""
    count = 0
    while len(cluster_member) != len_cluster:
        cluster = node_member[rd.randint(0, len(node_member) - 1)]

        if count < 2 and cluster not in cluster_member:
            cluster_member.append(cluster)
            node_member.remove(cluster)
        elif cluster not in cluster_member:
            cluster_member.append(cluster)
            node_member.remove(cluster)
        count += 1
    # split 2d list to 1d list
    cluster_x, cluster_y = zip(*cluster_member)
    return cluster_x, cluster_y, cluster_member


def cal_shot_distance(node_member, cluster_member, shot_dis_data):
    """find distance between node and cluster"""
    for node in range(len(node_member)):
        shot_dis = None  # shortest distance
        what_cluster = None  # what cluster?
        for cluster in range(len(cluster_member)):
            cal_distance = math.sqrt((node_member[node][0] - cluster_member[cluster][0]) ** 2 +
                                     (node_member[node][1] - cluster_member[cluster][1]) ** 2)
            # find shortest cluster
            if shot_dis is None:
                shot_dis = cal_distance
                what_cluster = cluster
            elif cal_distance < shot_dis:
                shot_dis = cal_distance
                what_cluster = cluster
        shot_dis_data.append([node, what_cluster, shot_dis])
    return shot_dis_data


def plot(shot_dis_data, node_member, cluster_member, clus_x, clus_y, base_x, base_y, node_x, node_y):
    """plot everything in graph"""
    # plot line between node and cluster
    for z in range(len(shot_dis_data)):
        plt.plot([node_member[shot_dis_data[z][0]][0], cluster_member[shot_dis_data[z][1]][0]],
                 [node_member[shot_dis_data[z][0]][1], cluster_member[shot_dis_data[z][1]][1]],
                 color='k', linestyle='-', linewidth=0.1)  # Black Line
    # plot node, base, cluster
    plt.plot(base_x[0:], base_y[0:], 'ro')  # base station
    plt.plot(node_x[0:], node_y[0:], 'bo')  # nodes
    plt.plot(clus_x[0:], clus_y[0:], 'go')  # cluster head
    plt.show()


def main(width, height, density, clus_density, num_base):
    """insert area and population of node and point of base station"""

    # variable
    node_member, cluster_member, station, shot_dis_data, len_nodes, len_cluster = variable(width, height, density,
                                                                                           clus_density)

    # set base_station
    station, base_x, base_y = base_station(num_base, station)

    # random_node
    node_member, node_x, node_y = random_node(node_member, len_nodes, width, height, station)

    # random_cluster
    cluster_x, cluster_y, cluster_member = random_cluster(cluster_member, len_cluster, node_member)

    # cal_shot_distance
    shot_dis_data = cal_shot_distance(node_member, cluster_member, shot_dis_data)

    # plot
    plot(shot_dis_data, node_member, cluster_member, cluster_x, cluster_y, base_x, base_y, node_x, node_y)


main(int(50),
     int(50),
     float(0.025),
     float(0.079),
     int(1))

# input("Width of this area (Meter) = ")
# input("Height of this area (Meter) = ")
# input("Node density (Node/Meter^2) = ")
# input("Cluster density (Cluster/Node) = ")
# input("How many Base Station in this area (Base Station) = ")
# input("X,Y coordinate of this base station "+str(item+1)+" = ")
