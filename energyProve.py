import sys
sys.path.append("..")

#import multiprocessing as mp
from multiprocessing import Process, Queue
import os
import matplotlib.pyplot as plt
import numpy as np
from energyUtils import *
from loraTheoricalSimulation import *

calc_semtech_power_mw = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
calc_semtech_power_dbm = [22, 23, 24, 24, 24, 25, 25, 25, 25, 26, 31, 32, 34, 35, 44, 82, 85, 90, 105, 115, 125]


sleep_power_in_ma = 0.001*voltage_supply # 1uA

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

def H1theoricalSimulatedHaza():
    
    h1tl = []
    h1sm = []
    for i in range(1, 12000, 400):
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

    plt.plot(distance, q1th, "b-", linewidth=1)
    plt.plot(distance, q1sm, "bo", linewidth=1)
    plt.plot(distance, h1th, "r-", linewidth=1)
    plt.plot(distance, h1sm, "ro")
    plt.plot(distance, c1t, "g-", linewidth=1)
    plt.ylim(0, 1.1)
    #plt.legend("H1 theorical outage", "Q1 theorical outage", "H1Q1 outage")

    plt.show()
if __name__== "__main__":
    
    #plotConsume1Day()
    plotC1tTheoricalSimulated()
    



"""
    sf8_energy_per_package = packageEnergyCalculator(get_toa(25, 8)['t_packet'], 14)
    sf8_one_day[0] = lifeTimeEnergyCalculator(test_time, 0.001281, sf8_energy_per_package, 10)
    sf8_one_day[1] = lifeTimeEnergyCalculator(test_time, 0.001281, sf8_energy_per_package, 100)
    sf8_one_day[2] = lifeTimeEnergyCalculator(test_time, 0.001281, sf8_energy_per_package, 1000)

    sf9_energy_per_package = packageEnergyCalculator(get_toa(25, 9)['t_packet'], 14)
    sf9_one_day[0] = lifeTimeEnergyCalculator(test_time, 0.001281, sf9_energy_per_package, 10)
    sf9_one_day[1] = lifeTimeEnergyCalculator(test_time, 0.001281, sf9_energy_per_package, 100)
    sf9_one_day[2] = lifeTimeEnergyCalculator(test_time, 0.001281, sf9_energy_per_package, 1000)

    sf10_energy_per_package = packageEnergyCalculator(get_toa(25, 10)['t_packet'], 14)
    sf10_one_day[0] = lifeTimeEnergyCalculator(test_time, 0.001281, sf10_energy_per_package, 10)
    sf10_one_day[1] = lifeTimeEnergyCalculator(test_time, 0.001281, sf10_energy_per_package, 100)
    sf10_one_day[2] = lifeTimeEnergyCalculator(test_time, 0.001281, sf10_energy_per_package, 1000)

    sf11_energy_per_package = packageEnergyCalculator(get_toa(25, 11)['t_packet'], 14)
    sf11_one_day[0] = lifeTimeEnergyCalculator(test_time, 0.001281, sf11_energy_per_package, 10)
    sf11_one_day[1] = lifeTimeEnergyCalculator(test_time, 0.001281, sf11_energy_per_package, 100)
    sf11_one_day[2] = lifeTimeEnergyCalculator(test_time, 0.001281, sf11_energy_per_package, 1000)
    
    sf12_energy_per_package = packageEnergyCalculator(get_toa(25, 12)['t_packet'], 14)
    sf12_one_day[0] = lifeTimeEnergyCalculator(test_time, 0.001281, sf12_energy_per_package, 10)
    sf12_one_day[1] = lifeTimeEnergyCalculator(test_time, 0.001281, sf12_energy_per_package, 100)
    sf12_one_day[2] = lifeTimeEnergyCalculator(test_time, 0.001281, sf12_energy_per_package, 1000)


    plt.bar((5,6,7), sf8_one_day, 0.5)
    plt.bar((10,11,12), sf9_one_day, 0.5)
    plt.bar((15,16,17), sf10_one_day, 0.5)
    plt.bar((20,21,22), sf11_one_day, 0.5)
    plt.bar((25,26,27), sf12_one_day, 0.5)
"""