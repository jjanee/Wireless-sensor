import matplotlib.pyplot as plt
import random as rd
import math 

def create_point():
    "insert area and population of node and point of base station"
    area_x = int(input("Enter width area = ")) #meter
    area_y = int(input("Enter height area = ")) #meter
    base_x, base_y, station = [], [], []
    node_member, cluster_member = [],[]
    distance, node_distance = [], []
    density = float(input("Enter destity of nodes = ")) #nodes/meter^2
    len_nodes = math.ceil(density*(area_x*area_y))
    num_base = int(input("How many base sation in area = "))
    
    for item in range (0, num_base): #input base station point
        station.append(map(int, input("Enter point of base station "+str(item+1)+" = ").split(',')))

    while(len(node_member) != len_nodes): #random Node
        node = [rd.randint(0,area_x), rd.randint(0,area_y)]
        if node not in node_member and node not in station :
            node_member.append(node)
    population = float(input("Enter population of cluster = "))
    population = math.ceil(population*len_nodes)
    
    while(len(cluster_member) != population): #random Cluster from amount Node
        cluster = node_member[rd.randint(0,len(node_member)-1)]
        cluster_member.append(cluster)
        node_member.remove(cluster)
    
    for node in range(len(node_member)):
        near_cluster = "none"
        for cluster in range(len(cluster_member)):
            cal_distance = math.sqrt((node_member[node][0] - cluster_member[cluster][0])**2+\
                                     (node_member[node][1] - cluster_member[cluster][1])**2)
            if near_cluster == "none"  :#ไปทุกโหนด
                near_cluster = cal_distance
                clus_num = cluster
            elif cal_distance < near_cluster and \
                 node_member[node] not in distance : 
                near_cluster = cal_distance
                clus_num = cluster
        plt.plot([node_member[node][0], cluster_member[clus_num][0]],\
                [node_member[node][1], cluster_member[clus_num][1]],\
                color='k', linestyle='-', linewidth=0.1)#สีดำ 

    clus_x, clus_y = zip(*cluster_member)
    node_x, node_y = zip(*node_member)
    base_x, base_y = zip(*station)
    plt.xlabel('width')
    plt.ylabel('height')
    plt.title('Wireless node')
    plt.grid(True)
    plt.plot(base_x[0:], base_y[0:], 'ro')#nodes
    plt.plot(node_x[0:], node_y[0:],'.')#nodes
    plt.plot(clus_x[0:], clus_y[0:], 'go')#cluster head
    plt.show()
    
create_point()
