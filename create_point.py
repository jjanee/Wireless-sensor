import matplotlib.pyplot as plt
import random as rd
import numpy 
import math 

def create_point():
    "insert area and population of node and point of base station"
    area_x = int(50) #meter
    area_y = int(50) #meter
    num_base = int(input(" How many base sation in area = "))
    station, ran_nodeX, ran_nodeY  = [],[],[]
    node_member, cluster_member = [],[]
    distance, node_distance = [], []
    density = float(0.025) #nodes/meter^2
    len_nodes = math.ceil(density*(area_x*area_y))
    
    for item in range (0, num_base): #input base station point
        station.append(input("Enter point of base station "+str(item+1)+" = ").split(','))

    population = float(input("cluster"))
    population = math.ceil(population*len_nodes)

    count = 0
    while(len(node_member) != len_nodes): #random Node
        ran_nodeX.append(rd.randint(0,area_x))
        ran_nodeY.append(rd.randint(0,area_y))
        node_member.append([ran_nodeX[count], ran_nodeY[count]])
        if [ran_nodeX[count], ran_nodeY[count]] not in node_member and \
           [ran_nodeX[count], ran_nodeY[count]] not in station and\
           count == 2:
            node_member.append([ran_nodeX[count], ran_nodeY[count]])
            cal_distance = math.sqrt((ran_nodeX[count] - ran_nodeX[count-1])**2+\
                                (ran_nodeY[count] - ran_nodeY[count-1])**2)
            print("cal = "+str(cal_distance))
        count += 1
        
        
    while(len(cluster_member) != population): #random Cluster from amount Node
        cluster = node_member[rd.randint(0,len(node_member)-1)]
        if cluster not in cluster_member :
            cluster_member.append(cluster)
            node_member.remove(cluster)
    
    for node in range(len(node_member)):
##        near_cluster = "none"
        for cluster in range(len(cluster_member)):
            cal_distance = math.sqrt((node_member[node][0] - cluster_member[cluster][0])**2+\
                                     (node_member[node][1] - cluster_member[cluster][1])**2)

        
##       plt.plot([node_member[node][0], cluster_member[cluster][0]],\
##                         [node_member[node][1], cluster_member[cluster][1]],\
##                         color='k', linestyle='-', linewidth=0.1)#สีดำ
       

            
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
    print(base_x)
    print(base_y)
    plt.plot(base_x[0:], base_y[0:],'ro')#nodes
    plt.plot(node_x[0:], node_y[0:],'bo')#nodes
    plt.plot(clus_x[0:], clus_y[0:], 'go')#cluster head
    plt.show()
    
create_point()
