import csv
import matplotlib.pyplot as plt
import random as rd
import math
import numpy as np
import pandas
from collections import Counter
import seaborn


def variable(width, height, density, cluster_density):
    """variables"""
    node_member, cluster_member, station_member, shot_dis_data = [], [], [], []
    len_nodes = math.ceil(density * (width * height))
    len_cluster = math.ceil(cluster_density * len_nodes)
    return node_member, cluster_member, station_member, shot_dis_data, len_nodes, len_cluster


def base_station(num_base, station_member):
    """input base station point"""
    for item in range(num_base):
        station_member.append(list(map(int, "50,-1".split(','))))

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
        random_x, random_y = [rd.randint(0, width), rd.randint(0, height)]
        if [random_x, random_y] not in node_member and \
                [random_x, random_y] not in station_member:
            node_member.append([random_x, random_y, 1])  # set energy = 1 Joule
        count += 1

    # append data to csv. file
    with open('node_member.csv', 'w', newline='') as csvnew:
        write = csv.writer(csvnew)
        for line in node_member:
            write.writerow(line)
    return node_member


def random_cluster(cluster_member, len_cluster, node_member, option, shot_dis_data):
    """random Cluster from amount Node"""
    print(str(len_cluster)+"******")
    if option == 0:
        while len(cluster_member) != len_cluster:
            cluster = node_member[rd.randint(0, len(node_member) - 1)][:2]
            if cluster not in cluster_member:
                cluster_member.append(cluster)

        # append data to csv. file
        with open('cluster_member.csv', 'w', newline='') as csvnew:
            write = csv.writer(csvnew)
            for line in cluster_member:
                write.writerow(line)

    elif option == 2:
        cluster_member = []
        count = 0
        while len(cluster_member) != len_cluster:
            cluster = node_member[rd.randint(0, len(node_member) - 1)][:2]
            for i in range(len(shot_dis_data)):
                if cluster not in cluster_member \
                        and int(shot_dis_data[i][1]) == count \
                        and float(shot_dis_data[i][2]) != 0.0:
                    cluster_member.append(cluster)
                    count += 1
        print(str(len(cluster_member))+"*******")

        # append data to csv. file
        with open('cluster_member.csv', 'w', newline='') as csvnew:
            write = csv.writer(csvnew)
            for line in cluster_member:
                write.writerow(line)

    return cluster_member


def cal_shot_distance(node_member, cluster_member, shot_dis_data, option):
    """find distance between node and cluster"""
    if option == 2:
        for node in range(len(node_member)):
            for cluster in range(len(cluster_member)):
                cal_distance = math.sqrt((node_member[node][0] - cluster_member[cluster][0]) ** 2 +
                                         (node_member[node][1] - cluster_member[cluster][1]) ** 2)
                if shot_dis_data[node][1] == cluster:
                    shot_dis_data[node][1] = [node, cluster, cal_distance]

    elif option == 0:
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


def cal_energy(node_member, cluster_member, shot_dis_data):
    """Calculate how much energy nodes use"""
    data = 500  # bit
    elec_tran = 50 * (10 ** (-9))  # 50 nanoj
    elec_rec = 50 * (10 ** (-9))  # พลังงานตอนรับ 50 nanoj
    fs = 10 * (10 ** (-12))  # 10 picoj
    mpf = 0.013 * (10 ** (-12))  # 0.013 picoj

    d_threshold = 0
    for i in range(len(shot_dis_data)):
        d_threshold += i
    d_threshold = d_threshold / len(shot_dis_data)

    # amount of data cluster node carry
    cluster_carry = []
    for j in range(len(cluster_member)):
        temp = 0
        for k in range(len(shot_dis_data)):
            if int(shot_dis_data[k][1]) == j and float(shot_dis_data[k][2]) != 0.0:
                temp += data
        cluster_carry.append(temp)

    #                           shot_dis_data = [0 nodes] [1 group] [2 distance]
    # calculate
    calculate = []
    for x in range(len(shot_dis_data)):
        distance = float(shot_dis_data[x][2])
        if distance == 0.0:  # cluster (receive nodes)
            print(cluster_carry)
            print(shot_dis_data[x][1])
            calculate.append(cluster_carry[int(shot_dis_data[x][1])] * elec_rec)
        elif distance < d_threshold:#nodes (tranfer nodes)
            calculate.append((elec_tran + (fs * (distance ** 2))) * data)
        elif distance >= d_threshold:#nodes (tranfer nodes)
            calculate.append((elec_tran + (mpf * (distance ** 4))) * data)

    # set current energy
    for e in range(len(shot_dis_data)):
        current_energy = node_member[e][2] - float(calculate[e])
        node_member[e][2] = current_energy
        print(node_member[e])
    return node_member


def plot(shot_dis_data, node_member, cluster_member, station_member, count_lap, option):
    """plot everything in graph"""
    # plot line between node and cluster
    plt.ion()  # make plt.close() can executed ***don't delete please
    for z in range(len(shot_dis_data)):
        if shot_dis_data[z][2] != 0:
            plt.plot([node_member[int(shot_dis_data[z][0])][0], cluster_member[int(shot_dis_data[z][1])][0]],
                     [node_member[int(shot_dis_data[z][0])][1], cluster_member[int(shot_dis_data[z][1])][1]],
                     color='k', linestyle='-', linewidth=0.1)  # Black Line

    # split 2d list to 1d list
    base_x, base_y = zip(*station_member)
    clus_x, clus_y = zip(*cluster_member)
    node_x, node_y, node_energy_cal = zip(*node_member)

    # plot node, base, cluster
    plt.axis('scaled')
    plt.xlabel('Width')
    plt.ylabel('Height')
    plt.title('Random Sensor')
    plt.grid(True)
    plt.plot(base_x[0:], base_y[0:], 'ro', markersize=3)  # base station
    plt.plot(node_x[0:], node_y[0:], 'bo', markersize=3)  # nodes
    plt.plot(clus_x[0:], clus_y[0:], 'go', markersize=3)  # cluster head
    if option == 0 or option == 1:
        plt.savefig("Figure_%s.png" % count_lap)
    elif option == 2:
        plt.savefig("Figure_%d.png" % (count_lap+1))
    plt.close()  # Don't delete it!


    keep = []
    node = []
    for index in shot_dis_data:
        keep.append("%.1f" % float(index[2]))
        node.append(int(index[1]))
    # "---------------------------------distance-------"
##    keep.sort()
##    ##    seaborn.set()
##    letter_counts = Counter(keep)
##    df = pandas.DataFrame.from_dict(letter_counts, orient='index')
##    df.plot(kind='bar', title='distance between node and cluster', colormap='jet')
##    plt.savefig('distance.png', dpi=1200)
##
##    # ---------------member of cluster ber round-------"
##    ##    node.sort()
##    letter_counts = Counter(node)
##    df = pandas.DataFrame.from_dict(letter_counts, orient='index')
##    df.plot(kind='bar', title='member of cluster per round', colormap='jet')
##    plt.savefig('member of cluster.png', dpi=1200)


def new_input(width, height, density, cluster_density, num_base, option):
    """insert area and population of node and point of base station"""

    node_member, cluster_member, station_member, shot_dis_data, len_nodes, len_cluster = \
        variable(width, height, density, cluster_density)  # variable

    node_member = random_node(node_member, len_nodes, width, height, station_member)  # random_node

    cluster_member = random_cluster(cluster_member, len_cluster, node_member, option, shot_dis_data)  # random_cluster

    station_member = base_station(num_base, station_member)  # set base_station

    shot_dis_data = cal_shot_distance(node_member, cluster_member, shot_dis_data, option)  # cal_shot_distance

    count_lap = "0"
    cal_energy(node_member, cluster_member, shot_dis_data)
    plot(shot_dis_data, node_member, cluster_member, station_member, count_lap, option)  # plot


def random_cluster_ingroup(option, lap):
    """only random new cluster from their own group"""
    # gain data from .csv files
    old_sdd, old_nm, old_cm, old_e, station_member = [], [], [], [], []
    with open("station_member.csv", 'r') as csvnew:
        read = csv.reader(csvnew)
        for line in read:
            station_member.append(list(map(int, line)))
    with open("node_member.csv", 'r') as csvnew:
        read = csv.reader(csvnew)
        for line in read:
            old_nm.append(list(map(int, line)))
    with open("cluster_member.csv", 'r') as csvnew:
        read = csv.reader(csvnew)
        for line in read:
            old_cm.append(list(map(int, line)))
    with open("shot_dis_data.csv", 'r') as csvnew:
        read = csv.reader(csvnew)
        for line in read:
            old_sdd.append(line)

    # loop with lap input
    count = 0
    for i in range(len(old_sdd)):
        if float(old_sdd[i][2]) == 0.0:
            count += 1
    len_cluster = count
    for count_lap in range(lap):
        # random_cluster
        cluster_member = random_cluster(old_cm, len_cluster, old_nm, option, old_sdd)

        # cal_shot_distance
        shot_dis_data = cal_shot_distance(old_nm, cluster_member, old_sdd, option)

        cal_energy(old_nm, cluster_member, shot_dis_data)

        # plot
        plot(shot_dis_data, old_nm, cluster_member, station_member, count_lap, option)

    # sort by group
    # shot_dis_data.sort(key=lambda x: int(x[1]))
    # for x in range(len(shot_dis_data)):
    #     print(shot_dis_data[x])


def current_data(option):
    """use current data not change anything"""
    # gain data from .csv files
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
    count_lap = "CURRENT_DATA"
    cal_energy(node_member, cluster_member, shot_dis_data)
    plot(shot_dis_data, node_member, cluster_member, station_member, count_lap, option)


def start():
    """Choose Functions"""
    print("Choose 0 new input")
    print("Choose 1 current data")
    print("Choose 2 random only cluster")
    option = int(input("----> "))

    if option == 0:  # new input
        new_input(int(50), int(50), float(0.025), float(0.079), int(1), option)
    elif option == 1:  # current data:
        current_data(option)
    elif option == 2:
        lap = int(input("how many lap do you need? : "))
        random_cluster_ingroup(option, lap)


start()

# input("Width of this area (Meter) = ")
# input("Height of this area (Meter) = ")
# input("Node density (Node/Meter^2) = ")
# input("Cluster density (Cluster/Node) = ")
# input("How many Base Station in this area (Base Station) = ")
# input("X,Y coordinate of this base station "+str(item+1)+" = ")
