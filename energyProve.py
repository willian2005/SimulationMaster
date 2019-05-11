import sys
sys.path.append("..")
sys.path.append("output_data/")

#import multiprocessing as mp
from multiprocessing import Process, Queue
import os
import matplotlib.pyplot as plt
import numpy as np
from energyUtils import *
from loraTheoricalSimulation import *
from devicesDistribuition import *
from CYCLES_100_PER_INTERACTION_100_Gx_12000_Gy_12000 import *

calc_semtech_power_mw = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
calc_semtech_power_dbm = [22, 23, 24, 24, 24, 25, 25, 25, 25, 26, 31, 32, 34, 35, 44, 82, 85, 90, 105, 115, 125]


sleep_power_in_ma = 0.001*voltage_supply # 1uA

def csvSaveData(gateway_possition, distance, h1sm, q1sm, c1t):

    text_name = "output_data/CYCLES_" + str(REPTION_TIMES_CYCLES) + "_PER_INTERACTION_" + str(REPTION_TIMES_PER_INTERACTION_Q1_SIM) + "_Gx_" + str(gateway_possition[0]) + "_Gy_" + str(gateway_possition[1]) + ".py"
    file = open(text_name, 'w')

    line = "distances_gx_" + str(gateway_possition[0]) + "_gy_" + str(gateway_possition[1]) + " = " + str(distance) + "\n" 
    file.write(line)
    line = "h1sm_gx_" + str(gateway_possition[0]) + "_gy_" + str(gateway_possition[1]) + " = " + str(h1sm) + "\n" 
    file.write(line)
    line = "q1sm_gx_" + str(gateway_possition[0]) + "_gy_" + str(gateway_possition[1]) + " = " + str(q1sm) + "\n" 
    file.write(line)
    line = "c1t_gx_" + str(gateway_possition[0]) + "_gy_" + str(gateway_possition[1]) + " = " + str(c1t) + "\n" 
    file.write(line)

def plotCalcSemtechPower_mA_by_dbm():
    plt.plot(calc_semtech_power_mw, calc_semtech_power_dbm)
    plt.xlabel('power in mA')
    plt.ylabel('power in dBm')
    plt.show()

def plotConsume1Day():

    plt.title('Energia gasta em 1 dia de operação, com 10, 100 ou 1000 mensagens enviadas - 25bytes/msg')
    test_time = 60*60*24
    sf_one_day = np.tile(0.0, 3)
    power_dbm = 14
    x = 0
    for i in range(7,13):
        sf_time_per_package = get_toa(25, i)['t_packet']
        sf_one_day[0] = lifeTimeWorkCalculator(test_time, sf_time_per_package, power_dbm, 10)
        sf_one_day[1] = lifeTimeWorkCalculator(test_time, sf_time_per_package, power_dbm, 100)
        sf_one_day[2] = lifeTimeWorkCalculator(test_time, sf_time_per_package, power_dbm, 1000)
        plt.bar((x,x+1,x+2), sf_one_day, 0.5)
        x = x+5
    
    plt.xticks((0,1, 2,6, 11, 16, 21, 26), ('10','100 \nSF7', '1000', 'SF8', 'SF9', 'SF10', 'SF11', 'SF12')) 
    plt.yscale('log')
    plt.ylabel('Energia em Joule')
    plt.xlabel('Mensagens enviadas por SF')
    plt.grid()
    plt.show()

def H1theoricalSimulatedHaza(max_distance = 12000):
    
    h1tl = []
    h1sm = []
    for i in range(1, max_distance, 400):
        if i < 2000:
            h1tl.append(H1Theorical(7, i))
            h1sm.append(H1Simulated(7, i))
        elif i < 4000: 
            h1tl.append(H1Theorical(8, i))
            h1sm.append(H1Simulated(8, i))
        elif i < 6000:
            h1tl.append(H1Theorical(9, i))
            h1sm.append(H1Simulated(9, i))
        elif i < 8000:
            h1tl.append(H1Theorical(10, i))
            h1sm.append(H1Simulated(10, i))
        elif i < 10000:
            h1tl.append(H1Theorical(11, i))
            h1sm.append(H1Simulated(11, i))
        else:
            h1tl.append(H1Theorical(12, i))
            h1sm.append(H1Simulated(12, i))

    return h1tl, h1sm

def plotShiftedDeviceDistribuition(max_distance = 12000, gateway= (12000,12000)):

    q1sm = np.zeros(round(max_distance/400))
    gateway_possition = gateway

    def processParallelQ1(distance, q, index):
        temp = Q1WithShiftedGateway(distance, 500, gateway_possition)
        q.put((index, temp))
        print("the distance: %d, outage: %f"% (distance, temp))
    
    distances = []
    index = 0
    q = Queue()
    for distance in range(1, max_distance, 400):
        
        p = Process(target=processParallelQ1, args=(distance, q, index)) 
        p.start()
        index = index +1
        print("Lauching the thread: %d"% index)
        distances.append(distance)
    p.join()
    
    for i in range(0, round(max_distance/400)):
        a = q.get()
        q1sm[a[0]] = a[1]
    
    return q1sm, distances

    

def plotDefaultDeviceDistribuition(gateway = (12000,12000)):
    
    devices_list, devices_per_circle  = averageDevicesDistribuition(500, gateway)

    plt.figure()
    #print(devices_list)
    for i in range(len(devices_list)):
        if devices_list[i][2] < 2000:
            plt.scatter(devices_list[i][0], devices_list[i][1], c="blue", linewidths=0.01)
        elif devices_list[i][2] < 4000: 
            plt.scatter(devices_list[i][0], devices_list[i][1], c="green", linewidths=0.01)
        elif devices_list[i][2] < 6000:
            plt.scatter(devices_list[i][0], devices_list[i][1], c="yellow", linewidths=0.01)
        elif devices_list[i][2] < 8000:
            plt.scatter(devices_list[i][0], devices_list[i][1], c="pink", linewidths=0.01)
        elif devices_list[i][2] < 10000:
            plt.scatter(devices_list[i][0], devices_list[i][1], c="black", linewidths=0.01)
        else:
            plt.scatter(devices_list[i][0], devices_list[i][1], c="brown", linewidths=0.01)

    plt.scatter(gateway[0], gateway[1],  c="red")
    plt.ylim(0, 24000)
    plt.xlim(0, 24000)
    #need because of the legend
    plt.scatter(-1, -1, c="red", linewidths=0.01, label='Gateway')
    plt.scatter(-1, -1, c="blue", linewidths=0.01, label='SF7')
    plt.scatter(-1, -1, c="green", linewidths=0.01, label='SF8')
    plt.scatter(-1, -1, c="yellow", linewidths=0.01, label='SF9')
    plt.scatter(-1, -1, c="pink", linewidths=0.01, label='SF10')
    plt.scatter(-1, -1, c="black", linewidths=0.01, label='SF11')
    plt.scatter(-1, -1, c="brown", linewidths=0.01, label='SF12')

    #plot the centralized circuference
    """for i in  range(0, 14000, 2000):
        circle= plt.Circle((12000,12000), fill=False, radius= i)
        ax=plt.gca()
        ax.add_patch(circle)
    """
    plt.legend(loc='upper right')
    plt.title("Distribuição dos dispositivos")
    plt.savefig("output_data/device_distribuition_CYCLES_" + str(REPTION_TIMES_CYCLES) + "_PER_INTERACTION_" + str(REPTION_TIMES_PER_INTERACTION_Q1_SIM) + "_Gx_" + str(gateway[0]) + "_Gy_" + str(gateway[1]) + ".png")
    #plt.show()

def Q1TheoricalSimulatedHaza():
    
    q1sm = np.zeros(30)

    def processParallelQ1(distance, q, index):
        temp = Q1Simulated(distance)
        q.put((index, temp))
        print("the distance: %d, outage: %f"% (distance, temp))
    
    q1t = []
    #q1sm = []
    distances = []
    index = 0
    q = Queue()
    for distance in range(1, 12000, 400):
        
        p = Process(target=processParallelQ1, args=(distance, q, index)) 
        p.start()
        index = index +1
        print("Lauching the thread: %d"% index)
    p.join()

    for i in range(0,30):
        a = q.get()
        q1sm[a[0]] = a[1]
    
    print(q1sm)

    for i in range(1, 12000, 400):
        q1t.append(Q1Theorical(i))
        distances.append(i)

    return q1t, q1sm, distances

def plotC1tTheoricalSimulated():

    [q1th, q1sm, distance] = Q1TheoricalSimulatedHaza()
    [h1th, h1sm] = H1theoricalSimulatedHaza()

    c1t = []

    for i in range(len(h1th)):
        c1t.append(h1th[i]*q1th[i])

    plt.plot(distance, q1th, "b-" ,linewidth=1)
    plt.plot(distance, q1sm, "bo", linewidth=1)
    plt.plot(distance, h1th, "r-", linewidth=1)
    plt.plot(distance, h1sm, "ro")
    plt.plot(distance, c1t, "g-", linewidth=1)
    plt.ylim(0, 1.1)
    #plt.legend("H1 theorical outage", "Q1 theorical outage", "H1Q1 outage")

    plt.show()



def plotC1tShiftedGateway(max_distance = 14000, gateway_possition= (12000,12000)):
    
    [q1sm, distance] = plotShiftedDeviceDistribuition(max_distance, gateway_possition)
    [h1th, h1sm] = H1theoricalSimulatedHaza(max_distance)

    plotDefaultDeviceDistribuition( gateway_possition)
    c1t = []
    for i in range(len(h1sm)):
        c1t.append(q1sm[i]*h1sm[i])

    plt.figure()
    plt.plot(distance, q1sm, "b-", label='Q1 Simulado', linewidth=1)
    plt.plot(distance, h1sm, "r-", label='H1 Simulado')
    plt.plot(distance, c1t, "g-", linewidth=1, label='Outage')
    plt.ylim(0, 1.1)

    plt.legend(loc='upper right')
    plt.title("Gateway em X: " + str(gateway_possition[0]) + " Y: " + str(gateway_possition[1]) )
    plt.savefig("output_data/plot_CYCLES_" + str(REPTION_TIMES_CYCLES) + "_PER_INTERACTION_" + str(REPTION_TIMES_PER_INTERACTION_Q1_SIM) + "_Gx_" + str(gateway_possition[0]) + "_Gy_" + str(gateway_possition[1]) + ".png")

    h1_list = [float(h1) for h1 in h1sm]
    q1_list = [float(q1) for q1 in q1sm]
    c1_list = [float(c1) for c1 in c1t]
    csvSaveData(gateway_possition, distance, h1_list, q1_list, c1_list)

def plotSavedData():

    plt.plot(distances_gx_12000_gy_12000, q1sm_gx_12000_gy_12000, "b-", label='Q1 Simulado', linewidth=1)
    plt.plot(distances_gx_12000_gy_12000, h1sm_gx_12000_gy_12000, "r-", label='H1 Simulado')
    plt.plot(distances_gx_12000_gy_12000, c1t_gx_12000_gy_12000, "g-", linewidth=1, label='Outage')
    plt.ylim(0, 1.1)

    plt.legend(loc='upper right')
    plt.show()

if __name__== "__main__":
    
    max_distance = 12000
    gateway= (12000,12000)
    plotC1tShiftedGateway(max_distance, gateway)

    max_distance = 14000
    gateway= (10000,12000)
    plotC1tShiftedGateway(max_distance, gateway)
    #plotDefaultDeviceDistribuition()

    #plotSavedData()
    #plotC1tTheoricalSimulated()