import sys
sys.path.append("..")

import matplotlib.pyplot as plt
import numpy as np
from energyUtils import *
from haza import *

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

def H1theoricalHaza():
    
    h1tl = []
    for i in range(1, 12000, 400):
        if i < 2000:
            h1tl.append(H1Theorical(7, i))
        elif i < 4000: 
            h1tl.append(H1Theorical(8, i))
        elif i < 6000:
            h1tl.append(H1Theorical(9, i))
        elif i < 8000:
            h1tl.append(H1Theorical(10, i))
        elif i < 10000:
            h1tl.append(H1Theorical(11, i))
        else:
            h1tl.append(H1Theorical(12, i))

    return h1tl

def Q1TheoricalHaza():
    
    q1t = []
    for i in range(1, 12000, 400):
        q1t.append(Q1Theorical(i))
    
    return q1t

def plotC1tTheoricalHaza():

    h = H1theoricalHaza()
    q = Q1TheoricalHaza()

    c1t = []
    for i in range(len(h)-1):
        c1t.append(h[i]*q[i])

    plt.plot(q, "b-", linewidth=1)
    plt.plot(h, "r-", linewidth=1)
    plt.plot(c1t, "g-", linewidth=1)
    plt.xlim(1, 12000)
    plt.show()
if __name__== "__main__":
    
    #plotH1theoricalHaza()
    plotC1tTheoricalHaza()
    



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