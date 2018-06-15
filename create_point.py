import matplotlib.pyplot as plt
import random as rd
import numpy 
from math import sqrt, ceil

def create_point():
    "insert area and population of node and point of base station"
    area_x = int(50) #meter
    area_y = int(50) #meter
    num_base = int(1)
    base_x, base_y, station = [], [], []
    ran_nodeX, ran_nodeY = [],[]
    node_member, cluster_member = [],[]
    node_distance = []
    density = float(0.025) #nodes/meter^2
    len_nodes = int(density*(area_x*area_y))

    for item in range (0, num_base): #input base station point
        base_x.append(int(input("Enter point x of base station "+str(item+1)+" = ")))
        base_y.append(int(input("Enter point y of base station "+str(item+1)+" = ")))
        station.append([base_x[item], base_y[item]])

    count = 0
    while(len(node_member) != len_nodes): #random Node
        ran_nodeX.append(rd.randint(0,area_x))
        ran_nodeY.append(rd.randint(0,area_y))  
        if [ran_nodeX[count], ran_nodeY[count]] not in node_member and \
           [ran_nodeX[count], ran_nodeY[count]] not in station :
            node_member.append([ran_nodeX[count], ran_nodeY[count]])
        count += 1

    while(len(cluster_member) != 5): #random Cluster from amount Node
        cluster = node_member[rd.randint(0,len(node_member)-1)]
        if cluster not in cluster_member:
            cluster_member.append(cluster)
            node_member.remove(cluster)

    for node in range(len(node_member)):
##        near_cluster = "none"
        for cluster in range(len(cluster_member)):
            cal_distance = sqrt((node_member[node][0] - cluster_member[cluster][0])**2+\
                                (node_member[node][1] - cluster_member[cluster][1])**2)
            node_distance.append([node_member[node], cluster_member[cluster], cal_distance])
        print(numpy.argmin(node_distance[node][2]))
            
##            #find shortest cluster **if cal_distance = 0 that's a Cluster
##            if near_cluster == "none" :#ไปทุกโหนด
##                near_cluster = cal_distance
##                clus_num = cluster
##            elif cal_distance < near_cluster:
##                near_cluster = cal_distance
##                clus_num = cluster
##                plt.plot([node_member[node][0], cluster_member[cluster][0]],\
##                         [node_member[node][1], cluster_member[cluster][1]],\
##                         color='k', linestyle='-', linewidth=0.1)#สีดำ

    clus_x, clus_y = zip(*cluster_member)
    node_x, node_y = zip(*node_member)
    base_x, base_y = zip(*station)
    plt.plot(base_x[0:], base_y[0:],'ro')#nodes
    plt.plot(node_x[0:], node_y[0:],'bo')#nodes
    plt.plot(clus_x[0:], clus_y[0:], 'go')#cluster head
    plt.show()
    
create_point()
