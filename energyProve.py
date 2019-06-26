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
from lorawan_toa.lorawan_toa import get_toa

calc_semtech_power_mw = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
calc_semtech_power_dbm = [22, 23, 24, 24, 24, 25, 25, 25, 25, 26, 31, 32, 34, 35, 44, 82, 85, 90, 105, 115, 125]


sleep_power_in_ma = 0.001*voltage_supply # 1uA

def csvSaveData(gateway_possition, distance, h1sm, q1sm, c1t):

    text_name = "output_data/CYCLES_" + str(REPTION_TIMES_CYCLES) + "_PER_INTERACTION_" + str(REPTION_TIMES_PER_INTERACTION_Q1_SIM) + "_Gx_" + str(gateway_possition[0]) + "_Gy_" + str(gateway_possition[1]) + "_TOA_M_" + str(TOA_METHOD) + ".py"
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
def printTOA():
    
    sf_time_per_package = []
    for i in range(7,13):
        sf_time_per_package.append(get_toa(25, i)['t_packet'])
        #print("O tempo no ar SF%d é de: %fms e taxa de dados %f bytes/seg"%(i, sf_time_per_package, ((1000/(sf_time_per_package*100))*25)))
    print(sf_time_per_package)
    for i in range(len(sf_time_per_package)):
        print("SF%d - quantidade de vezes maior %f"% (i+7 ,sf_time_per_package[len(sf_time_per_package)-1]/sf_time_per_package[i]) )

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

def H1graphics(max_distance = 12000):
    
    h1 = [0]*6
    
    for i in range(6):
        h1[i] = []
    distance = []
    
    for i in range(1, max_distance, 400):
        
        h1[0].append(H1Theorical(7, i))
        h1[1].append(H1Theorical(8, i))
        h1[2].append(H1Theorical(9, i))
        h1[3].append(H1Theorical(10, i))
        h1[4].append(H1Theorical(11, i))
        h1[5].append(H1Theorical(12, i))
        distance.append(i)

    plt.plot(distance, h1[0], "b-" ,label = "SF7", linewidth=1)
    plt.plot(distance, h1[1], "g-" ,label = "SF8",linewidth=1)
    plt.plot(distance, h1[2], "y-" ,label = "SF9",linewidth=1)
    plt.plot(distance, h1[3], "r-" ,label = "SF10",linewidth=1)
    plt.plot(distance, h1[4], "m-" ,label = "SF11",linewidth=1)    
    plt.plot(distance, h1[5], "k-" ,label = "SF12",linewidth=1)
    plt.legend(loc='upper right')
    plt.title("Capacidade da comunicação H1")
    plt.xlabel("Distancia")
    plt.ylabel("Capacidade")
    plt.show()

def Q1Graphic():
    
    q1 = []
    number_of_devices = []

    for nd in range(2, 200, 3):
        temp = Q1OutageProbability(3000, nd)
        number_of_devices.append(nd)
        q1.append(temp)
        print("Devices %d - capacidade %f"%(nd, temp))
    plt.plot(number_of_devices, q1, "b-")
    plt.title("Capacidade de comunicação Q1")
    plt.xlabel("Numero de dispositivos")
    plt.ylabel("Capacidade")
    plt.show()

def H1theoricalSimulatedHaza(max_distance = 12000):
    
    h1tl = []
    h1sm = []

    for i in range(1, max_distance, 400):
        [sf, int_sf] = getSF(i)
        h1tl.append(H1Theorical(int_sf, i))
        h1sm.append(H1Simulated(int_sf, i))
    
    return h1tl, h1sm

def Q1ShiftedGateway(max_distance = 12000, gateway= [(12000,12000)], number_of_devices = 500):

    q1sm = np.zeros(round(max_distance/400))
    gateway_possition = gateway

    def processParallelQ1(distance, q, index):
        temp = Q1WithShiftedGateway(distance, number_of_devices, gateway_possition, max_distance)
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
        if index == 4:
            p.join()
            index = 0
    p.join()
    
    for i in range(0, round(max_distance/400)):
        a = q.get()
        q1sm[a[0]] = a[1]
    
    return q1sm, distances

def plotStorageQ1MultiplesGateways():

    device = DeviceDistribuition(1000, [(6000,12000), (18000, 12000)])
    """
    device.loadObjectData("output_data/DeviceDistribuition_poor_simulation2019-06-18_22:57.plt")
    print(device.getDeviceInEachSF())
    device.plotDevices("Distribuicao por SF")
    device.plotQ1Devices("DER Q1")
    device.plotQ1Histogram("Histograma da DER por SFs")
    H1IndividualDevices(device)
    device.plotH1Devices("H1 test")
    """
    device.loadObjectData("output_data/DeviceDistribuition_poor_simulation2019-06-18_16:26.plt")
    print(device.getDeviceInEachSF())
    device.plotDevices("Distribuicao por SF")
    """
    device.plotQ1Devices("DER Q1")
    device.plotQ1Histogram("Histograma da DER por SFs")
    """
    H1IndividualDevices(device)
    device.plotH1Devices("H1 test")

    device.loadObjectData("output_data/DeviceDistribuition_poor_simulation2019-06-18_18:18.plt")
    print(device.getDeviceInEachSF())
    device.plotDevices("Distribuicao por SF")
    device.plotQ1Devices("DER Q1")
    device.plotQ1Histogram("Histograma da DER por SFs")
"""
    device.loadObjectData("output_data/DeviceDistribuition_poor_simulation2019-06-16_20:12.plt")
    print(device.getDeviceInEachSF())
    device.plotDevices("Distribuicao por SF")
    device.plotQ1Devices("DER Q1")
    device.plotQ1Histogram("Histograma da DER por SFs")
"""
def plotC1MultiplesGateway(gateways = [(6000,12000), (18000, 12000)], number_of_devices = 4000):

    devices_to_be_analized = DeviceDistribuition(number_of_devices, gateways)

    devices_to_be_analized.averageDevicesDistribuition()
    devices_to_be_analized.plotDevices("teste")
    print(devices_to_be_analized.getDeviceInEachSF())
    

    number_of_interferents = number_of_devices

    Q1IndividualDevices(devices_to_be_analized)
    H1IndividualDevices(devices_to_be_analized)
    devices_to_be_analized.updateC1Probability()

    devices_to_be_analized.saveObjectData("c1_simulation")


def plotQ1MultiplesGateway(gateways = [(6000,12000), (18000, 12000)], number_of_devices = 4000):
    
    devices_to_be_analized = DeviceDistribuition(1000, gateways)

    devices_to_be_analized.averageDevicesDistribuition()
    devices_to_be_analized.plotDevices("teste")
    print(devices_to_be_analized.getDeviceInEachSF())
    

    number_of_interferents = number_of_devices

    Q1IndividualDevices(devices_to_be_analized, number_of_interferents, gateways)

    devices_to_be_analized.saveObjectData("poor_simulation")

    #debug
    #for device in devices_list:
    #    print(getDeviceDistancesFromGateways(device))
    #    print("x:%d - y:%d"%(getDeviceX(device), getDeviceY(device)))
    #print(devices_per_circle)

    return

def plotH1MultiplesGateway(gateways = [(6000,12000), (18000, 12000)], number_of_devices = 4000):

    
    devices_to_be_analized = DeviceDistribuition(number_of_devices, gateways)

    devices_to_be_analized.averageDevicesDistribuition(gateways)
    devices_to_be_analized.plotDevices("teste")
    print(devices_to_be_analized.getDeviceInEachSF())
    
    H1IndividualDevices(devices_to_be_analized)

    devices_to_be_analized.saveObjectData("H1_simulation")

    devices_to_be_analized.plotH1Devices("H1 test")
    #debug
    #for device in devices_list:
    #    print(getDeviceDistancesFromGateways(device))
    #    print("x:%d - y:%d"%(getDeviceX(device), getDeviceY(device)))
    #print(devices_per_circle)

    return

def plotDefaultDeviceDistribuition(gateways = [(6000,12000), (18000, 12000)], number_of_devices = 4000):
    
    devices = DeviceDistribuition(number_of_devices, gateways)
    devices.averageDevicesDistribuition()
    
    SF_list = ["SF7", "SF8", "SF9", "SF10", "SF11", "SF12"]
    SFs = []
    
    SFs = devices.getDeviceInEachSF()
    print(SF_list)
    print(SFs)    
    
    plt.figure()
    #print(devices_list)
    for i in range(devices.getNumberOfDevices() - 1):
        if devices.getSFName(i) == "SF7":
            plt.scatter(devices.getX(i), devices.getY(i), c="blue", linewidths=0.01)
        elif devices.getSFName(i) == "SF8": 
            plt.scatter(devices.getX(i), devices.getY(i), c="green", linewidths=0.01)
        elif devices.getSFName(i) == "SF9":
            plt.scatter(devices.getX(i), devices.getY(i), c="yellow", linewidths=0.01)
        elif devices.getSFName(i) == "SF10":
            plt.scatter(devices.getX(i), devices.getY(i), c="pink", linewidths=0.01)
        elif devices.getSFName(i) == "SF11":
            plt.scatter(devices.getX(i), devices.getY(i), c="black", linewidths=0.01)
        elif devices.getSFName(i) == "SF12":
            plt.scatter(devices.getX(i), devices.getY(i), c="brown", linewidths=0.01)

    for gateway in gateways:
        plt.scatter(gateway[0], gateway[1], c="red")
        print("Gateway = (%d, %d)"%(gateway[0], gateway[1]))
    
    plt.ylim(0, 24000)
    plt.xlim(0, 24000)
    #need because of the legend
    plt.scatter(-100, -1, c="red", linewidths=0.01, label='Gateway')
    plt.scatter(-100, -1, c="blue", linewidths=0.01, label='SF7')
    plt.scatter(-100, -1, c="green", linewidths=0.01, label='SF8')
    plt.scatter(-100, -1, c="yellow", linewidths=0.01, label='SF9')
    plt.scatter(-100, -1, c="pink", linewidths=0.01, label='SF10')
    plt.scatter(-100, -1, c="black", linewidths=0.01, label='SF11')
    plt.scatter(-100, -1, c="brown", linewidths=0.01, label='SF12')

    #plot the centralized circuference
    """for i in  range(0, 14000, 2000):
        circle= plt.Circle((12000,12000), fill=False, radius= i)
        ax=plt.gca()
        ax.add_patch(circle)
    """
    plt.legend(loc='upper right')
    plt.title("Distribuição dos dispositivos")
    plt.savefig("output_data/device_distribuition_CYCLES_" + str(REPTION_TIMES_CYCLES) + "_PER_INTERACTION_" + str(REPTION_TIMES_PER_INTERACTION_Q1_SIM) + "_Gx_" + str(gateway[0]) + "_Gy_" + str(gateway[1]) + "_TOA_M_" + str(TOA_METHOD) + ".png")

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

    plt.show()

def plotC1tShiftedGateway(max_distance = 12000, gateway_possition= (12000,12000), number_of_devices=500):
    
    [q1sm, distance] = Q1ShiftedGateway(max_distance, gateway_possition, number_of_devices)
    [h1th, h1sm] = H1theoricalSimulatedHaza(max_distance)

    plotDefaultDeviceDistribuition( gateway_possition, number_of_devices)
    c1t = []
    for i in range(len(h1sm)):
        c1t.append(q1sm[i]*h1sm[i])

    plt.figure()
    plt.plot(distance, q1sm, "b-", label='Q1 Simulado', linewidth=1)
    plt.plot(distance, h1sm, "r-", label='H1 Simulado')
    plt.plot(distance, c1t, "g-", linewidth=1, label='Outage')
    plt.ylim(0, 1.1)

    plt.legend(loc='upper right')
    #plt.title("Gateway em X: " + str(gateway_possition[0]) + " Y: " + str(gateway_possition[1]) )
    plt.savefig("output_data/plot_CYCLES_" + str(REPTION_TIMES_CYCLES) + "_PER_INTERACTION_" + str(REPTION_TIMES_PER_INTERACTION_Q1_SIM) + "_Gx_" + str(gateway_possition[0][0]) + "_Gy_" + str(gateway_possition[0][1]) + "_TOA_M_" + str(TOA_METHOD) + ".png")

    h1_list = [float(h1) for h1 in h1sm]
    q1_list = [float(q1) for q1 in q1sm]
    c1_list = [float(c1) for c1 in c1t]
    csvSaveData(gateway_possition[0], distance, h1_list, q1_list, c1_list)

if __name__== "__main__":

    #plotQ1MultiplesGateway()
    #plotH1MultiplesGateway()
    #plotStorageQ1MultiplesGateways()
    #printTOA()   
    #Q1Graphic ()
    #H1graphics()

    
    #plotQ1MultiplesGateway(gateways = [(12000,12000)])
    plotC1MultiplesGateway(gateways = [(6000,12000), (18000, 12000)])
    #plotQ1MultiplesGateway(gateways = [(6000,6000), (18000, 6000), (12000,18000)])
    #plotQ1MultiplesGateway(gateways = [(6000,6000), (18000, 6000), (6000, 18000), (18000, 18000)])
    
    
    
    #plotDefaultDeviceDistribuition([(6000,12000), (18000, 12000)], 4000)
    #plotDefaultDeviceDistribuition([(6000,6000), (18000, 6000), (6000, 18000), (18000, 18000)], 4000)
    
    #max_distance = 12000
    #gateway= [(6000,12000), ((18000,12000)) ]
    #plotDefaultDeviceDistribuitionMultiplesGateway([(6000, 12000), (18000, 12000)], 4000)

    """
    max_distance = 14000
    gateway= [(10000,12000)]
    plotC1tShiftedGateway(max_distance, gateway)
    
    max_distance = 16000
    gateway= (8000,12000)
    plotC1tShiftedGateway(max_distance, gateway)

    max_distance = 18000
    gateway= (6000,12000)
    plotC1tShiftedGateway(max_distance, gateway)

    max_distance = 20000
    gateway= (4000,12000)
    plotC1tShiftedGateway(max_distance, gateway)
    """
    """
    plotDefaultDeviceDistribuition((12000,12000), 4000)
    plotDefaultDeviceDistribuition((10000,12000))
    plotDefaultDeviceDistribuition((8000,12000))
    plotDefaultDeviceDistribuition((6000,12000))
    plotDefaultDeviceDistribuition((4000,12000))
    """
    #plotDefaultDeviceDistribuition()

    #plotSavedData()
    #plotC1tTheoricalSimulated()
