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
        random_x, random_y, energy = [rd.randint(0, width), rd.randint(0, height), 1]
        if [random_x, random_y, energy] not in node_member and \
                [random_x, random_y] not in station_member:
            node_member.append([random_x, random_y, energy])  # set energy = 1 Joule
        count += 1

    # append data to csv. file
    with open('node_member.csv', 'w', newline='') as csvnew:
        write = csv.writer(csvnew)
        for line in node_member:
            write.writerow(line)
    return node_member


def random_cluster(cluster_member, len_cluster, node_member, option, shot_dis_data):
    """random Cluster from amount Node"""
    # print(str(len_cluster)+"******")
    if option == 0:
        while len(cluster_member) != len_cluster:
            cluster = node_member[rd.randint(0, len(node_member) - 1)][:2]
            if cluster not in cluster_member:
                cluster_member.append(cluster)

    elif option == 2 or option == 1:
        # print("old" + str(cluster_member))
        count = 0

        cluster_member = []
        while count != len_cluster:
            # for i in range(len(shot_dis_data)):
            #     if int(shot_dis_data[i][1]) == count:
            #         print(shot_dis_data[i][1:2], end='')
            #         print("  "+str(node_member[i]))
            c2 = None
            ttl = 0
            while c2 != count:
                cluster = shot_dis_data[rd.randint(0, len(node_member) - 1)]
                # print(cluster[1],end='')
                # print("*"+str(node_member[int(cluster[0])]))
                if int(cluster[1]) == count \
                        and float(cluster[2]) != 0.0 \
                        and float(node_member[int(cluster[0])][2]) > 0.0:  # protect from select dead nodes
                    cluster_member.append(node_member[int(cluster[0])][:2])
                    c2 = count
                    print(shot_dis_data[int(cluster[0])][1:2], end='')
                    print(node_member[int(cluster[0])])
                elif int(cluster[1]) == count \
                        and float(node_member[int(cluster[0])][2]) > 0.0:  # when only 1 nodes left
                    cluster_member.append(node_member[int(cluster[0])][:2])
                    c2 = count
                    print(shot_dis_data[int(cluster[0])][1:2], end='')
                    print(node_member[int(cluster[0])])
                elif int(cluster[1]) == count \
                        and ttl >= (len(node_member)*len_cluster):  # every nodes dead
                    cluster_member.append(node_member[int(cluster[0])][:2])
                    c2 = count
                    print(shot_dis_data[int(cluster[0])][1:2], end='')
                    print(node_member[int(cluster[0])])
                ttl += 1
            count += 1
        print("-------------^cluster^-------------")

    # append data to csv. file
    with open('cluster_member.csv', 'w', newline='') as csvnew:
        write = csv.writer(csvnew)
        for line in cluster_member:
            write.writerow(line)

    return cluster_member, len_cluster


def cal_shot_distance(node_member, cluster_member, shot_dis_data, option, count_lap):
    """find distance between node and cluster"""
    # print("****************************---------------------------------********************************")
    keep_distance = []
    if option == 2 or option == 1 and count_lap != 0:
        for cluster in range(len(cluster_member)):
            for node in range(len(node_member)):
                cal_distance = math.sqrt((node_member[node][0] - cluster_member[cluster][0]) ** 2 +
                                         (node_member[node][1] - cluster_member[cluster][1]) ** 2)
                keep_distance.append([cal_distance])
                if int(shot_dis_data[node][1]) == cluster:
                    shot_dis_data[node] = [shot_dis_data[node][0], shot_dis_data[node][1], cal_distance]
    elif option == 0:
        for node in range(len(node_member)):
            shot_dis = None  # shortest distance
            what_cluster = None  # what cluster?
            for cluster in range(len(cluster_member)):
                cal_distance = math.sqrt((node_member[node][0] - cluster_member[cluster][0]) ** 2 +
                                         (node_member[node][1] - cluster_member[cluster][1]) ** 2)
                keep_distance.append([cal_distance])# find shortest cluster
                if shot_dis is None:
                    shot_dis = cal_distance
                    what_cluster = cluster
                elif cal_distance < shot_dis:
                    shot_dis = cal_distance
                    what_cluster = cluster
            shot_dis_data.append([node, what_cluster, shot_dis])

    # count = 0
    # while count != len(cluster_member):
    #     for i in range(len(shot_dis_data)):
    #         if int(shot_dis_data[i][1]) == count:
    #             print(node_member[i][:2], end='')
    #             print(shot_dis_data[i])
    #     count += 1
    #     print("---------------------------------------------")

    # append data to csv. file
    with open('shot_dis_data.csv', 'w', newline='') as csvnew:
        write = csv.writer(csvnew)
        for line in shot_dis_data:
            write.writerow(line)
    with open('keep_distance.csv', 'a', newline='') as csvnew:
        write = csv.writer(csvnew)
        for line in keep_distance:
            write.writerow(line)
    return shot_dis_data


def cal_energy(node_member, cluster_member, shot_dis_data, count_lap):
    """Calculate how much energy nodes use"""
    data = 1500000  # bit
    elec_tran = 50 * (10 ** (-9))  # 50 nanoj
    elec_rec = 50 * (10 ** (-9))  # พลังงานตอนรับ 50 nanoj
    fs = 10 * (10 ** (-12))  # 10 picoj
    mpf = 0.013 * (10 ** (-12))  # 0.013 picoj

    count = 0
    while count != len(cluster_member):
        for i in range(len(shot_dis_data)):
           if int(shot_dis_data[i][1]) == count:
               print(shot_dis_data[i][1:2], end='')
               print("  " + str(node_member[i]))
        count += 1
        print("------------------------------------------")

    d_threshold = 0
    for i in range(len(shot_dis_data)):
        d_threshold += i
    d_threshold = d_threshold / len(shot_dis_data)

    # amount of data cluster node carry
    cluster_carry = []
    for j in range(len(cluster_member)):
        temp = 0
        for k in range(len(shot_dis_data)):
            if int(shot_dis_data[k][1]) == j \
                    and float(shot_dis_data[k][2]) != 0.0 \
                    and float(node_member[k][2] > 0.0):
                temp += data
        cluster_carry.append(temp)
    print(cluster_carry)

    dead_nodes = 0
    if sum(cluster_carry) == 0:
        dead_nodes = 1
    # shot_dis_data = [0 nodes] [1 group] [2 distance]
    # calculate

    calculate = []
    for x in range(len(shot_dis_data)):
        distance = float(shot_dis_data[x][2])
        if distance == 0.0:  # cluster (receive nodes)
            cal_1 = cluster_carry[int(shot_dis_data[x][1])] * elec_rec
            calculate.append(cal_1)
        elif distance < d_threshold:  # nodes (tranfer nodes)
            cal_2 = (elec_tran + (fs * (distance ** 2))) * data
            calculate.append(cal_2)
        elif distance >= d_threshold:  # nodes (tranfer nodes)
            cal_3 = (elec_tran + (mpf * (distance ** 4))) * data
            calculate.append(cal_3)

    # set current energy, check dead nodes
    for e in range(len(shot_dis_data)):
        # print(calculate[e])
        current_energy = node_member[e][2] - float(calculate[e])
        if current_energy <= 0.0:
            node_member[e][2] = 0.0
        else:
            node_member[e][2] = current_energy
        # print(shot_dis_data[e], end='')
        # print("     "+ str(node_member[e][2]))
    # print(dead_nodes)
    print("LAP : " + str(count_lap))
    print("*************************************************************")
    return node_member, dead_nodes


def plot(shot_dis_data, node_member, cluster_member, station_member, count_lap, option, keep_distance):
    """plot everything in graph"""
    # plot line between node and cluster
    plt.ion()  # make plt.close() can executed ***don't delete please
    for z in range(len(shot_dis_data)):
        if shot_dis_data[z][2] != 0 and float(node_member[z][2]) > 0.0:            plt.plot([node_member[int(shot_dis_data[z][0])][0], cluster_member[int(shot_dis_data[z][1])][0]],
                     [node_member[int(shot_dis_data[z][0])][1], cluster_member[int(shot_dis_data[z][1])][1]],
                     color='k', linestyle='-', linewidth=0.5)  # Black Line
        elif shot_dis_data[z][2] != 0 and float(node_member[z][2]) == 0.0:
            plt.plot([node_member[int(shot_dis_data[z][0])][0], cluster_member[int(shot_dis_data[z][1])][0]],
                     [node_member[int(shot_dis_data[z][0])][1], cluster_member[int(shot_dis_data[z][1])][1]],
                     color='r', linestyle='-', linewidth=0.2)  # Red Line
        # print(shot_dis_data[z][2])
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


    if option == 2 or option == 1:
        plt.savefig("Figure_%d.png" % (count_lap))
    # thinking for option 1
    plt.close()  # Don't delete it!


    keep = []
    for index in keep_distance:
        keep.append(float("%.2f" % float(index[0])))
    plt.xlabel('distance')
    plt.ylabel('amount of nodes')
    plt.title('distance between cluster and nodes sensor')
    plt.hist(keep ,bins = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70])
    plt.savefig("distance.png")
    plt.close()


def new_input(width, height, density, cluster_density, num_base, option):
    """insert area and population of node and point of base station"""

    node_member, cluster_member, station_member, shot_dis_data, len_nodes, len_cluster = \
        variable(width, height, density, cluster_density)  # variable

    node_member = random_node(node_member, len_nodes, width, height, station_member)  # random_node

    cluster_member, len_cluster = random_cluster(cluster_member, len_cluster, node_member, option, shot_dis_data)  # random_cluster

    station_member = base_station(num_base, station_member)  # set base_station

    count_lap = 0
    shot_dis_data = cal_shot_distance(node_member, cluster_member, shot_dis_data, option, count_lap)  # cal_shot_distance


def random_cluster_ingroup(option, lap):
    """only random new cluster from their own group"""
    # gain data from .csv files
    old_sdd, old_nm, old_cm, old_e, station_member, keep_distance = [], [], [], [], [], []
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
    with open("keep_distance.csv", 'r') as csvnew:
        read = csv.reader(csvnew)
        for line in read:
            keep_distance.append(line)

    # loop with lap input
    count = 0
    for i in range(len(old_sdd)):
        if float(old_sdd[i][2]) == 0.0:
            count += 1
    len_cluster = count

    if option == 2:
        for count_lap in range(lap):
            cluster_member, len_cluster = random_cluster(old_cm, len_cluster, old_nm, option, old_sdd)

            shot_dis_data = cal_shot_distance(old_nm, cluster_member, old_sdd, option, count_lap)

            node_member, dead_nodes = cal_energy(old_nm, cluster_member, shot_dis_data, count_lap)

            plot(shot_dis_data, node_member, cluster_member, station_member, count_lap, option, keep_distance)
    else:
        count_lap = 1
        while True:
            cluster_member, len_cluster = random_cluster(old_cm, len_cluster, old_nm, option, old_sdd)

            shot_dis_data = cal_shot_distance(old_nm, cluster_member, old_sdd, option, count_lap)

            node_member, dead_nodes = cal_energy(old_nm, cluster_member, shot_dis_data, count_lap)

            plot(shot_dis_data, node_member, cluster_member, station_member, count_lap, option, keep_distance)

            count_lap += 1

            if dead_nodes == 1:
                break
    # sort by group
    # shot_dis_data.sort(key=lambda x: int(x[1]))
    # for x in range(len(shot_dis_data)):
    #     print(shot_dis_data[x])


def start():
    """Choose Functions"""
    print("Choose 0 set new input")
    print("Choose 1 loop cluster until every node dead")
    print("Choose 2 loop cluster up on you")
    option = int(input("----> "))

    if option == 0:  # new input
        new_input(int(50), int(50), float(0.025), float(0.079), int(1), option)
    elif option == 1:  # current data:
        lap = None
        random_cluster_ingroup(option, lap)
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
