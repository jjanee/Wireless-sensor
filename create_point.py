import matplotlib.pyplot as plt
import numpy as np

def create_point():
    "insert area and population of node and point of base station"
    area_x = int(input("Enter widht area = "))
    area_y = int(input("Enter hight area = "))
    num_base = int(input("How many base do you want = "))
    base_x ,base_y = [], []
    for i in range (0, num_base):
        base_x.append(int(input("Enter point x of base station "+str(i+1)+"= ")))
        base_y.append(int(input("Enter point y of base station "+str(i+1)+"= ")))
    population = float(input("Enter poppulation of node in area = "))
    cluster = float(input("Enter population of cluster in area ="))
    int_popu = int(population*area_x*area_y)
              #np.random.random_integers(max,size=(node,1)) 
    point_x = np.random.random_integers(area_x,size=(int_popu,1))
    point_y = np.random.random_integers(area_y,size=(int_popu,1))
    plt.plot(point_x[0:], point_y[0:],'bo')#node
    plt.plot(base_x[0:] , base_y[0:], 'go')#base station
    plt.show()

    # test การ commit
create_point()
