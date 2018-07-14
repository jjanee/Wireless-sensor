import pandas 
import matplotlib.pyplot as plt
import random as rd
import math
import numpy as np


def variable(width, height, density, cluster_density):
    """variables"""
    node_member, cluster_member, station_member, \
                 node_energy, shot_dis_data = [], [], [], [], []
    len_nodes = math.ceil(density * (width * height))
    len_cluster = math.ceil(cluster_density * len_nodes)
    return node_member, cluster_member, station_member, shot_dis_data, len_nodes, len_cluster, node_energy


def base_station(num_base, station_member):
    """input base station point"""
    for item in range(num_base):
        station_member.append(list(map(int, "51,-1".split(','))))

    print(pd.__version__)

    writer = pd.ExcelWriter('test.xlsx', engine='xlsxwriter')
    workbook  = writer.book
    ws = workbook.add_worksheet('mytab')

    ws.write(1,1,'This is a test')

    writer.close()


    # append data to csv. file
    with open('station_member.csv', 'w', newline='') as csvnew:
        write = csv.writer(csvnew)
        for line in station_member:
            write.writerow(line)
    return station_member


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
