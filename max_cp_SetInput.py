import matplotlib.pyplot as plt
import random as rd
import math 

def whole_system(width, height, density, clus_density, num_base):
    "insert area and population of node and point of base station"
    
    #variables
    node_member, cluster_member, station, shot_dis_data = [], [], [], []
    len_nodes = math.ceil(density*(width*height))
    len_cluster = math.ceil(clus_density*len_nodes)
    #input base station point
    for item in range(num_base): 
        station.append(map(int,"51,-1".split(',')))


    #random Node
    count = 0
    while(len(node_member) != len_nodes): 
        ran_nodex, ran_nodey = rd.randint(0,width), rd.randint(0,height)
        if [ran_nodex, ran_nodey] not in node_member and\
           [ran_nodex, ran_nodey] not in station :
            node_member.append([ran_nodex, ran_nodey])
        count += 1


    #random Cluster from amount Node  
    count = 0    
    while(len(cluster_member) != len_cluster): 
        cluster = node_member[rd.randint(0,len(node_member)-1)]
        
        if count < 2 and cluster not in cluster_member:
            cluster_member.append(cluster)
            node_member.remove(cluster)
        elif cluster not in cluster_member :
            cluster_member.append(cluster)
            node_member.remove(cluster)
        count += 1
    
    
    #split 2-metric list to 1-metric list
    clus_x, clus_y = zip(*cluster_member)
    node_x, node_y = zip(*node_member)
    base_x, base_y = zip(*station)
    
        
    #find distance between node and cluster
    for node in range(len(node_member)):
        shot_dis = None #shotest distance
        what_clus = None #what cluster?
        for cluster in range(len(cluster_member)):
            cal_distance = math.sqrt((node_member[node][0] - cluster_member[cluster][0])**2+\
                                     (node_member[node][1] - cluster_member[cluster][1])**2)
            #find shortest cluster
            if shot_dis == None :
                shot_dis = cal_distance
                what_clus = cluster
            elif cal_distance < shot_dis:
                shot_dis = cal_distance
                what_clus = cluster
        shot_dis_data.append([node, what_clus, shot_dis])
    
    
    #plot line between node and cluster
    for z in range(len(shot_dis_data)):
        plt.plot([node_member[shot_dis_data[z][0]][0], cluster_member[shot_dis_data[z][1]][0]],\
                 [node_member[shot_dis_data[z][0]][1], cluster_member[shot_dis_data[z][1]][1]],\
                 color='k', linestyle='-', linewidth=0.1)#สีดำ
    #plot node, base, cluster
    plt.plot(base_x[0:], base_y[0:],'ro')#base station
    plt.plot(node_x[0:], node_y[0:],'bo')#nodes
    plt.plot(clus_x[0:], clus_y[0:],'go')#cluster head
    plt.show()
    
whole_system(int(50),
             int(50),
             float(0.025),
             float(0.079),
             int(1))

#input("Width of this area (Meter) = ")
#input("Height of this area (Meter) = ")
#input("Node density (Node/Meter^2) = ")
#input("Cluster density (Cluster/Node) = ")
#input("How many Base Station in this area (Base Station) = ")
#input("X,Y coordinate of this base station "+str(item+1)+" = ")
