#! /usr/bin/python3
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
from loraInterativeSimulation import *
from devicesDistribuition import *
from lorawan_toa.lorawan_toa import get_toa
from operator import truediv
import optparse

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
def simulateC1MultiplesGateway(gateways, number_of_devices, radius, save_data, sf_method, device_power, power_method, h1_target):

    devices_to_be_analized = DeviceDistribuition(number_of_devices, gateways, radius, sf_method, device_power, power_method, h1_target)

    devices_to_be_analized.averageDevicesDistribuition()
    devices_to_be_analized.plotDevices("Device Distribuition")
    devices_to_be_analized.plotDevicesPower("Power of devices", "max_min")
    print(devices_to_be_analized.getDeviceInEachSF())
    
    Q1IndividualDevices(devices_to_be_analized)
    H1IndividualDevices(devices_to_be_analized)
    devices_to_be_analized.updateC1Probability()

    devices_to_be_analized.saveObjectData(save_data)

def plotEnergyConsumption(distribuition_object_path, payload_size, package_per_day, battery, tx_mode):

    device_distribuition = DeviceDistribuition()
    #calcule
    # - Average power in each SF
    # - Average power of all devices in network
    # - Average of life time in each SF
    # - Average of life time of all devices in network
    
    device_distribuition = DeviceDistribuition()
    device_distribuition.loadObjectData(distribuition_object_path)
    average_power_per_sf = sum_power_per_sf = 6*[0]
    average_life_time_per_sf = sum_life_time_per_sf = 6*[0]
    average_network_power = sum_network_power = 0
        
    for i in range(sum(device_distribuition.getDeviceInEachSF())):
        toa = get_toa(payload_size, device_distribuition.getSFNumber(i))['t_packet']
        power_per_package = packageWorkCalculator(toa, device_distribuition.getTransmissionPower(i))
        life_time_device, one_day_work = batteryTimeOfLife(battery, package_per_day, toa, device_distribuition.getTransmissionPower(i), tx_mode)
#        print("SF %d, one_day_work %f"%(device_distribuition.getSFNumber(i), one_day_work))
        sum_network_power = sum_network_power+power_per_package
        sf_base = device_distribuition.getSFNumber(i) - 7

        sum_power_per_sf[sf_base] = sum_power_per_sf[sf_base] + power_per_package
        sum_life_time_per_sf[sf_base] = sum_life_time_per_sf[sf_base] + life_time_device

    average_network_power = sum_network_power/sum(device_distribuition.getDeviceInEachSF())
    average_power_per_sf = list(map(truediv, sum_power_per_sf, device_distribuition.getDeviceInEachSF()))
    average_life_time_per_sf = list(map(truediv, sum_life_time_per_sf, device_distribuition.getDeviceInEachSF()))

    average_power_per_sf_formated = ['%.3f'%elem for elem in average_power_per_sf]
    average_life_time_per_sf_formated = ['%.3f' % elem for elem in average_life_time_per_sf]
    sum_power_per_sf_formated = ['%.3f' % elem for elem in sum_power_per_sf]

    print("Package - Average power per SF\n", average_power_per_sf_formated)
    print("Package - Sum power per SF (1 package per device)\n", sum_power_per_sf_formated)
    print("Package - Average network power \n%.3f"% average_network_power)
    print("Package - Sum network power (1 package per device)\n%.3f"% sum_network_power)
    print("Life time per SF\n", average_life_time_per_sf_formated)

def plotDeviceDistribuition(distribuition_object_path, plot_range_method):

    device_distribuition = DeviceDistribuition()
    device_distribuition.loadObjectData(distribuition_object_path)
    print(device_distribuition.getDeviceInEachSF())
    device_distribuition.plotDevices("Device Distribuition")
    device_distribuition.plotDevicesPower("Power of devices", plot_range_method)
    device_distribuition.plotH1Devices("DER H1 distribuition", plot_range_method)
    device_distribuition.plotQ1Devices("DER Q1 distribuition", plot_range_method)
    device_distribuition.plotC1Devices("DER C1 distribuition", plot_range_method)

    device_distribuition.plotC1Histogram("DER Histogram")

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
    
def checkGatewaysIsInsideRadius(gateways, radius_size):

    ret = True
    x_central_point = radius_size
    y_central_point = radius_size
    
    for gw in gateways:
        x_distance = abs(gw[0] - x_central_point)
        y_distance = abs(gw[1] - y_central_point)
        distance = math.sqrt(x_distance**2 + y_distance**2)
        #print("Distance to gateway: %f", distance)
        if(distance > radius_size):
            ret = False
    
    return ret


if __name__== "__main__":

    parser = optparse.OptionParser( usage="Ex: ./energyProve.py --simulate --gateway=\"[|1500,2250|, |1500, 750|]\" --number_of_devices=500 --radius_size=3000")

    parser.add_option('--simulate',
        action="store_true", dest="simulate",
        help="Simulate the network with the parameters, can't be used with --plot", 
        default=False)

    parser.add_option('--plot',
        action="store_true", dest="plot",
        help="Plot the data in a object device ditribuition,  should used with parameter, --plot_object_device_distribuition", 
        default=False)
    
    #TODO - implement independent from --plot
    parser.add_option('--energy_consumption',
        action="store_true", dest="energy_consumption",
        help="Calculate the energy used by each group of SF devices, should be used with --plot", 
        default=False)

    parser.add_option('--package_per_day',
        action="store", dest="package_per_day",
        help="Is the number of package sended by the day, the default is 100, should be used with --energy_consumption", 
        default=100)
    
    parser.add_option('--battery',
        action="store", dest="battery",
        help="Is the charge of a battery (in Joules), the default is 13320, used to calculate the life time of device, should be used with --energy_consumption", 
        default=13320)

    parser.add_option('--tx_mode',
        action="store", dest="tx_mode",
        help="Is the number of rx windows in receive data, could be \"tx\", \"tx_rx\", \"tx_rx_rx\", the default is \"tx\", used to calculate the life time of device, should be used with --energy_consumption", 
        default="tx")

    parser.add_option('--payload_size',
        action="store", dest="payload_size",
        help="Is the size of payload, the default is 25, should be used with --energy_consumption", 
        default=25)


    parser.add_option('--sf_method',
        action="store", dest="sf_method",
        help="Method used to set the SFs, could be: \"RADIAL\", \"SAME_TIME_ON_AIR\"", 
        default="RADIAL")

    parser.add_option('--number_of_devices',
        action="store", dest="number_of_devices",
        help="Number of devices in the network", 
        default=False)

    parser.add_option('--radius_size',
        action="store", dest="radius_size",
        help="The total radius of the network", 
        default=False)
    
    parser.add_option('--save_object_device_distribuition',
        action="store", dest="save_object_device_distribuition",
        help="Save the object of the class device distribuition on file \"arg\"", 
        default="der")

    parser.add_option('--plot_object_device_distribuition',
        action="store", dest="plot_object_device_distribuition",
        help="Plot the object of the class device distribuition on file \"arg\"", 
        default=False)

    parser.add_option('--gateways',
        action="store", dest="gateways",
        help="list of gateways, ex:  \"[|X1,Y1|, |X2, Y2|]\", should be used with parameter --simulate",
        default=False)

    parser.add_option('--device_power_variable',
        action="store", dest="device_power_variable",
        help="Set the power of the device, if not set the default is 19dBm. The options are: power_fullrange and power_lora_range.\
        Power fullrange try to set the H1 to --h1_target (default = 0.9), to do it, change the power of device with analog values. \
        Lora range, try to set the H1 to --h1_target (default = 0.9), set the power of the device in values possible by LoRa.", 
        default=False)

    parser.add_option('--h1_target',
        action="store", dest="h1_target",
        help="Set the power of the device to reach the H1 in the value set", 
        default=0.9)

    parser.add_option('--h1_mult_gateway_diversity',
        action="store", dest="h1_mult_gateway_diversity",
        help="Set the power of the device to reach the H1 in the value set", 
        default=false)

    parser.add_option('--plot_range',
        action="store", dest="plot_range",
        help="Define the way that the range of plots should be showed, options: 1_min, max_min\
        Should be used with --plot.",
        default="1_min")


    
    options, args = parser.parse_args()
    
    if(options.simulate == True):
        print("Init the simulation with the parameters")

        if(options.device_power_variable != False):
            
            device_power = 0
            if options.device_power_variable == "power_fullrange":
                power_method = "FULL_RANGE"
            elif options.device_power_variable == "power_lora_range":
                power_method = "LORA_RANGE"
            else:
                print("Power method is unknow, the options are: --device_power_variable=\"power_fullrange\" \
                and --device_power_variable=\"power_lora_range\"")
                exit(-1)
        else:
            power_method = "STATIC"
            device_power = 14 
        
        if( float(options.h1_target) > 0 and float(options.h1_target) < 1):
                h1_target = float(options.h1_target)
        else:
            print("H1_target is out of acceptable range.")
            exit(-1)
            
        if(options.gateways != False):
            string_gateways = options.gateways
            gateways = []
        else:
            print("To run the simulation you need to specify the gateways")
            print(options.gateways)
            exit(-1)
        
        if(options.number_of_devices != False):
            number_of_devices = int(options.number_of_devices)
        else:
            print("To run the simulation you need to specify the number of devices")
            exit(-1)
        
        if(options.radius_size != False):
            radius_size = int(options.radius_size)
        else: 
            print("To run the simulation you need to specify the radius size")
            exit(-1)
            
        try:
            for part_str in string_gateways.split("|"):
                if(len(part_str) > 2):
                    x = int(part_str.split(",")[0])
                    y = int(part_str.split(",")[1])
                    gateways.append((x, y))
                
        except ValueError:
            print("The sintax of variable --gateway is wrong, use ex: ./energyProve.py --simulate --gateway=\"[|6000,12000|, |18000, 12000|]\"")
    
        print("List of gateways")
        print(gateways)
    
        if options.simulate and checkGatewaysIsInsideRadius(gateways, radius_size) == False :
            print("The gateways is out of circle")
            exit(-1)

        simulateC1MultiplesGateway(gateways, number_of_devices, radius_size, options.save_object_device_distribuition, options.sf_method, device_power, power_method, h1_target)

    elif(options.plot == True ):

        object_path = options.plot_object_device_distribuition

        print("Plot the data in the file: %s" % object_path)
        if(options.energy_consumption == True):
            plotEnergyConsumption(object_path, options.payload_size, options.package_per_day, options.battery, options.tx_mode)
        
        if(options.plot_range != "1_min" and options.plot_range != "max_min" ):
            print("Option --plot_range with wrong value. \
            The options are --plot_range=\"1_min\" or --plot_range=\"max_min\" ")
            print("Using the value, %s"%options.plot_range)
            exit(-1)

        plotDeviceDistribuition(object_path, options.plot_range)


    #plotQ1MultiplesGateway()
    #plotH1MultiplesGateway()
    #plotStorageQ1MultiplesGateways()
    #printTOA()   
    #Q1Graphic ()
    #H1graphics()

    #plotQ1MultiplesGateway(gateways = [(12000,12000)])

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


"""LIMBO

def plotStorageQ1MultiplesGateways():

    device = DeviceDistribuition(1000, [(6000,12000), (18000, 12000)])
    
    #device.loadObjectData("output_data/DeviceDistribuition_poor_simulation2019-06-18_22:57.plt")
    #print(device.getDeviceInEachSF())
    #device.plotDevices("Distribuicao por SF")
    #device.plotQ1Devices("DER Q1")
    #device.plotQ1Histogram("Histograma da DER por SFs")
    #H1IndividualDevices(device)
    #device.plotH1Devices("H1 test")
    
    device.loadObjectData("output_data/DeviceDistribuition_poor_simulation2019-06-18_16:26.plt")
    print(device.getDeviceInEachSF())
    device.plotDevices("Distribuicao por SF")
    
    #device.plotQ1Devices("DER Q1")
    #device.plotQ1Histogram("Histograma da DER por SFs")
    
    H1IndividualDevices(device)
    device.plotH1Devices("H1 test")

    device.loadObjectData("output_data/DeviceDistribuition_poor_simulation2019-06-18_18:18.plt")
    print(device.getDeviceInEachSF())
    device.plotDevices("Distribuicao por SF")
    device.plotQ1Devices("DER Q1")
    device.plotQ1Histogram("Histograma da DER por SFs")

    #device.loadObjectData("output_data/DeviceDistribuition_poor_simulation2019-06-16_20:12.plt")
    #print(device.getDeviceInEachSF())
    #device.plotDevices("Distribuicao por SF")
    #device.plotQ1Devices("DER Q1")
    #device.plotQ1Histogram("Histograma da DER por SFs")



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
    #for i in  range(0, 14000, 2000):
    #    circle= plt.Circle((12000,12000), fill=False, radius= i)
    #    ax=plt.gca()
    #    ax.add_patch(circle)
    #
    plt.legend(loc='upper right')
    plt.title("Distribuição dos dispositivos")
    plt.savefig("output_data/device_distribuition_CYCLES_" + str(REPTION_TIMES_CYCLES) + "_PER_INTERACTION_" + str(REPTION_TIMES_PER_INTERACTION_Q1_SIM) + "_Gx_" + str(gateway[0]) + "_Gy_" + str(gateway[1]) + "_TOA_M_" + str(TOA_METHOD) + ".png")


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

"""