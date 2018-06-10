import matplotlib.pyplot as plt
import random as rd
from math import sqrt

def create_point():
    "insert area and population of node and point of base station"
    area_x = int(5) #meter
    area_y = int(5) #meter
    num_base = int(3)
    base_x, base_y, station = [], [], []
    ran_nodeX, ran_nodeY = [],[]
    node_member, cluster_member = [],[]
    list_distance = []
    density = float(0.5) #nodes/meter^2
    len_nodes = int(density*(area_x*area_y))

    for item in range (0, num_base):
        base_x.append(int(input("Enter point x of base station "+str(item+1)+"= ")))
        base_y.append(int(input("Enter point y of base station "+str(item+1)+"= ")))
        station.append([base_x[item], base_y[item]])
    count = 0
    while(len(node_member) != len_nodes): #random Node
        ran_nodeX.append(rd.randint(0,area_x))
        ran_nodeY.append(rd.randint(0,area_y))  
        if [ran_nodeX[count], ran_nodeY[count]] not in node_member and \
           [ran_nodeX[count], ran_nodeY[count]] not in station :
            node_member.append([ran_nodeX[count], ran_nodeY[count]])
        count += 1

    while(len(cluster_member) != 3): #random Cluster from amount Node
        temp1e = node_member[rd.randint(0,len(node_member)-1)]
        if temp1e not in cluster_member:
            cluster_member.append(temp1e)   

    for x in range(len(node_member)):
        near_cluster = "none"
        for x2 in range(len(cluster_member)):
            cal_distance = sqrt((node_member[x][0] - cluster_member[x2][0])**2\
                                + (node_member[x][1] - cluster_member[x2][1])**2)
            
            #find shortest cluster **if cal_distance = 0 that's a Cluster
            if near_cluster == "none":
                near_cluster = cal_distance
                clus_num = x2
            elif cal_distance < near_cluster:
                near_cluster = cal_distance
                clus_num = x2

    clu_x, clu_y = zip(*cluster_member)
    nod_x, nod_y = zip(*node_member)
    plt.plot(base_x[0:], base_y[0:],'ro')#nodes
    plt.plot(nod_x[0:], nod_y[0:],'bo')#nodes
    plt.plot(clu_x[0:] , clu_y[0:], 'go')#cluster
    plt.show()
    
create_point()
