import csv
import matplotlib.pyplot as plt
import random as rd
import math


def variable(width, height, density, cluster_density):
    """variables"""
    node_member, cluster_member, station_member, shot_dis_data = [], [], [], []
    len_nodes = math.ceil(density * (width * height))
    len_cluster = math.ceil(cluster_density * len_nodes)
    return node_member, cluster_member, station_member, shot_dis_data, len_nodes, len_cluster


def base_station(num_base, station_member):
    """input base station point"""
    for item in range(num_base):
        station_member.append(list(map(int, "51,-1".split(','))))
    # append data to csv. file
    with open('station_member.csv', 'w', newline='') as csvnew:
        write = csv.writer(csvnew)
        for line in station_member:
             write.writerow(line)
    return station_member


def random_node(node_member, len_nodes, width, height, station_member):
    """random Node"""
    count = 0
    while len(node_member) != len_nodes:
        random_x, random_y = rd.randint(0, width), rd.randint(0, height)
        if [random_x, random_y] not in node_member and \
                [random_x, random_y] not in station_member:
            node_member.append([random_x, random_y])
        count += 1
    # append data to csv. file
    with open('node_member.csv', 'w', newline='') as csvnew:
        write = csv.writer(csvnew)
        for line in node_member:
            write.writerow(line)
    return node_member


def random_cluster(cluster_member, len_cluster, node_member):
    """random Cluster from amount Node"""
    while len(cluster_member) != len_cluster:
        cluster = node_member[rd.randint(0, len(node_member) - 1)]
        if cluster not in cluster_member:
            cluster_member.append(cluster)
    # append data to csv. file
    with open('cluster_member.csv', 'w', newline='') as csvnew:
        write = csv.writer(csvnew)
        for line in cluster_member:
            write.writerow(line)
    return cluster_member


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
        # append data to csv. file
        with open('shot_dis_data.csv', 'w', newline='') as csvnew:
            write = csv.writer(csvnew)
            for line in shot_dis_data:
                write.writerow(line)
    return shot_dis_data


def plot(shot_dis_data, node_member, cluster_member, station_member):
    """plot everything in graph"""
    # plot line between node and cluster
    for z in range(len(shot_dis_data)):
        if shot_dis_data[z][2] != 0:
            plt.plot([node_member[int(shot_dis_data[z][0])][0], cluster_member[int(shot_dis_data[z][1])][0]],
                     [node_member[int(shot_dis_data[z][0])][1], cluster_member[int(shot_dis_data[z][1])][1]],
                     color='k', linestyle='-', linewidth=0.1)  # Black Line
    # split 2d list to 1d list
    base_x, base_y = zip(*station_member)
    clus_x, clus_y = zip(*cluster_member)
    node_x, node_y = zip(*node_member)
    # plot node, base, cluster
    plt.axis('scaled')
    plt.xlabel('Width')
    plt.ylabel('Height')
    plt.title('Random Sensor')
    plt.grid(True)
    plt.plot(base_x[0:], base_y[0:], 'ro', markersize=3)  # base station
    plt.plot(node_x[0:], node_y[0:], 'bo', markersize=3)  # nodes
    plt.plot(clus_x[0:], clus_y[0:], 'go', markersize=3)  # cluster head
    plt.show()



def new_input(width, height, density, cluster_density, num_base):
    """insert area and population of node and point of base station""" 
    
    # variable
    node_member, cluster_member, station_member, shot_dis_data, len_nodes, len_cluster = variable(width, height, density
                                                                                                  , cluster_density)

    # random_node
    node_member = random_node(node_member, len_nodes, width, height, station_member)

    # random_cluster
    cluster_member = random_cluster(cluster_member, len_cluster, node_member)

    # set base_station
    station_member = base_station(num_base, station_member)

    # cal_shot_distance
    shot_dis_data = cal_shot_distance(node_member, cluster_member, shot_dis_data)


    # plot
    plot(shot_dis_data, node_member, cluster_member, station_member)


def random_cluster_ingroup():
    """only random new cluster from their own group"""
    #gain data from .csv files
    shot_dis_data, node_member, cluster_member, station_member = [], [], [], []
    with open("station_member.csv", 'r') as csvnew:
        read = csv.reader(csvnew)
        for line in read:
            station_member.append(list(map(int, line)))
    with open("node_member.csv", 'r') as csvnew:
        read = csv.reader(csvnew)
        for line in read:
            node_member.append(list(map(int, line)))
    with open("cluster_member.csv", 'r') as csvnew:
        read = csv.reader(csvnew)
        for line in read:
            cluster_member.append(list(map(int, line)))
    with open("shot_dis_data.csv", 'r') as csvnew:
        read = csv.reader(csvnew)
        for line in read:
            shot_dis_data.append(line)
    # sort by group
    # shot_dis_data.sort(key=lambda x: int(x[1]))
    # for x in range(len(shot_dis_data)):
    #     print(shot_dis_data[x])



def current_data():
    """use current data not change anything"""
    #gain data from .csv files
    shot_dis_data, node_member, cluster_member, station_member = [], [], [], []
    with open("station_member.csv", 'r') as csvnew:
        read = csv.reader(csvnew)
        for line in read:
            station_member.append(list(map(int, line)))
    with open("node_member.csv", 'r') as csvnew:
        read = csv.reader(csvnew)
        for line in read:
            node_member.append(list(map(int, line)))
    with open("cluster_member.csv", 'r') as csvnew:
        read = csv.reader(csvnew)
        for line in read:
            cluster_member.append(list(map(int, line)))
    with open("shot_dis_data.csv", 'r') as csvnew:
        read = csv.reader(csvnew)
        for line in read:
            shot_dis_data.append(line)
    # plot
    plot(shot_dis_data, node_member, cluster_member, station_member)


def start():
    """Choose Functions"""
    option = int(input("0,1,2 : "))
    if option == 0:  # new input
        new_input(int(50),
                  int(50),
                  float(0.025),
                  float(0.079),
                  int(1))
    elif option == 1:  # current data:
        current_data()
    elif option == 2:
        random_cluster_ingroup()

start()


# input("Width of this area (Meter) = ")
# input("Height of this area (Meter) = ")
# input("Node density (Node/Meter^2) = ")
# input("Cluster density (Cluster/Node) = ")
# input("How many Base Station in this area (Base Station) = ")
# input("X,Y coordinate of this base station "+str(item+1)+" = ")
