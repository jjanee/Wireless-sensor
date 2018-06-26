import matplotlib.pyplot as plt
import random as rd
import math 

def create_point():
    "insert area and population of node and point of base station"
    area_x = int(40) #meter
    area_y = int(40) #meter
#    num_base = int(input(" How many base sation in area = "))
    station, ran_nodeX, ran_nodeY  = [],[],[]
    node_member, cluster_member = [],[]
    density = float(0.025) #nodes/meter^2
    len_nodes = math.ceil(density*(area_x*area_y))
    
#    for item in range (0, num_base): #input base station point
#        station.append(input("Enter point of base station "+str(item+1)+" = ").split(','))

    clus_density = float(0.08)
    len_cluster = math.ceil(clus_density*len_nodes)

    count = 0
    while(len(node_member) != len_nodes): #random Node
        ran_nodeX.append(rd.randint(0,area_x))
        ran_nodeY.append(rd.randint(0,area_y))
        if [ran_nodeX[count], ran_nodeY[count]] not in node_member and \
          [ran_nodeX[count], ran_nodeY[count]] not in station :
            node_member.append([ran_nodeX[count], ran_nodeY[count]])
        count += 1
        
    count = 0    
    while(len(cluster_member) != len_cluster): #random Cluster from amount Node
        cluster = node_member[rd.randint(0,len(node_member)-1)]
        
        if count < 2 and cluster not in cluster_member:
            cluster_member.append(cluster)
            node_member.remove(cluster)
        elif cluster not in cluster_member :
            cluster_member.append(cluster)
            node_member.remove(cluster)
        count += 1
        
    
    for node in range(len(node_member)):
        shot_dis = None #shotest distance
        what_clus = None #what cluster?
        for cluster in range(len(cluster_member)):
            cal_distance = math.sqrt((node_member[node][0] - cluster_member[cluster][0])**2+\
                                     (node_member[node][1] - cluster_member[cluster][1])**2)
            print(cal_distance)
        

            
        #find shortest cluster
            if shot_dis == None :
                shot_dis = cal_distance
                what_clus = cluster
            elif cal_distance < shot_dis:
                shot_dis = cal_distance
                what_clus = cluster
        #create line between node and cluster
        plt.plot([node_member[node][0], cluster_member[what_clus][0]],\
                 [node_member[node][1], cluster_member[what_clus][1]],\
                 color='k', linestyle='-', linewidth=0.1)#สีดำ
        print(what_clus)
        print(str(shot_dis)+"   SHORTEST")
        print("***")

    clus_x, clus_y = zip(*cluster_member)
    node_x, node_y = zip(*node_member)
    base_x, base_y = zip(*station)
    plt.plot(base_x[0:], base_y[0:],'ro')#base station
    plt.plot(node_x[0:], node_y[0:],'bo')#nodes
    plt.plot(clus_x[0:], clus_y[0:],'go')#cluster head
    plt.show()
    
create_point()
