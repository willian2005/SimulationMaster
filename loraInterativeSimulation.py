import math 
from mpmath import *
import numpy as np
from random import randint

from loraSpecific import *
from mathUtils import *
from linkBudget import friisEquation
from devicesDistribuition import *

import multiprocessing 
from multiprocessing import Process, Queue

REPTION_TIMES = 10000
REPTION_TIMES_PER_INTERACTION_Q1_SIM = 1000
REPTION_TIMES_CYCLES = 1000


DEVICES_WITH_SAME_BAUDRATE      = 1     #All the SFs will transmit with the baudrate of the SF12
DEVICES_WITH_SAME_TIME_ON_AIR   = 2     #All the devices will transmit respecting the 1% rule (or less), SF7 will have higher baudrate 

TOA_METHOD = DEVICES_WITH_SAME_BAUDRATE

def radiusPerDistance( distance, max_distance):
        
    #    Return the minimum radius and maximum radius to the same SF
    
    l0 = last_distance_of_sf[-1]
    l1 = max_distance
    in_radius = 0
    for i in range(len(last_distance_of_sf)):

        if distance < last_distance_of_sf[i]:

            if(i == 0):
                l0 = 1
            else:
                l0 = last_distance_of_sf[i - 1]

            l1 = last_distance_of_sf[i]
            in_radius = i +1            
            break
    #print("i %d - distance %d - l0 %d - l1 %d - in_radius %d"% (i, distance,  l0, l1, in_radius)) 
    return l0, l1, in_radius

def getDevicesInTx(number_of_devices, method=DEVICES_WITH_SAME_BAUDRATE, sf=7):
    
    #get the number of devices that is transmitting in the same time
    devices_in_tx = 0
    if(method == DEVICES_WITH_SAME_TIME_ON_AIR):
        time_using_channel = randint(1, 100) #using a channel in 1% of the time
        for i in range(number_of_devices):
            if randint(1, 100) == time_using_channel:
                devices_in_tx = devices_in_tx + 1
    
    elif(method == DEVICES_WITH_SAME_BAUDRATE):
    
        time_on_air_in_reference_sf7 = round(time_on_air_in_reference_sf7_list[sf-7]*100)
        time_using_channel = randint(1, time_on_air_in_reference_sf7)#using a channel in 1% of the time
        #print("time_on_air_in_reference_sf7: %d, time_using_channel: %d"%(time_on_air_in_reference_sf7, time_using_channel))
        for i in range(number_of_devices):

            if randint(1, time_on_air_in_reference_sf7) == time_using_channel:
                devices_in_tx = devices_in_tx + 1
    
    return devices_in_tx
 
def H1IndividualDevices(devices_to_be_analized, n=2.75, bw = 125e3):

    
    for idx in range(devices_to_be_analized.getNumberOfDevices() - 1):

        print("PT TX %d", devices_to_be_analized.getTransmissionPower(idx))
        pw_tx = (10**(devices_to_be_analized.getTransmissionPower(idx)/10))/1e3
        sensibility = (10**(loraSensitivity(devices_to_be_analized.getSFNumber(idx), bw)/10))/1e3
        sum = 0

        for i in range(REPTION_TIMES):
            
            for idx_gw, gateway in enumerate(devices_to_be_analized.getGateways()):

                h_d1 = math.sqrt(0.5)*abs(np.random.randn(1) + np.random.randn(1)*j )
                if (float(pw_tx*friisEquation(int(devices_to_be_analized.getDeviceDistancesFromGateways(idx)[idx_gw]), n)*h_d1**2)) >= sensibility:
                    sum = sum + 1
                    break

        print("sum %d", sum/REPTION_TIMES)
        devices_to_be_analized.setH1Probability(idx, sum/REPTION_TIMES)
    return 

def Q1IndividualDevices(devices_to_be_analized, n=2.75):

    #devices_to_be_analized.plotDevices("devices to be analized")

    devices_outages = [0]*devices_to_be_analized.getNumberOfDevices()


    for cycle in range(REPTION_TIMES_CYCLES):  
        
        print(cycle)

        devices_interferents = devices_to_be_analized
        #devices_interferents.averageDevicesDistribuition(gateways)
        sqrt_0_5 = math.sqrt(0.5)
        rx_success_total = 0.0

        for idx in range(devices_to_be_analized.getNumberOfDevices() - 1):
            
            rx_success_total = 0
            sf_main_dev = devices_to_be_analized.getSFNumber(idx)
            sf_idx_interferents = devices_interferents.getDevicesSameSF(sf_main_dev)
            #get the number of devices that is transmitting in the same time
            number_devices_in_tx = getDevicesInTx(len(sf_idx_interferents), sf=sf_main_dev)
            
            if(number_devices_in_tx > 0):
                
                interfent_in_tx_list = []
                for i in range(number_devices_in_tx):
                    
                    dev_int_same_sf_list = devices_interferents.getDevicesSameSF(sf_main_dev)
                    idx_int = randint(0, len(dev_int_same_sf_list) - 1)
                    interfent_in_tx_list.append(dev_int_same_sf_list[idx_int])
                #simulate if you have success in the communication, considering the transmission signal of the interferents
                #print("SF - %d, number_devices_in_tx - %d"%(sf_main_dev, number_devices_in_tx))
                #print(interfent_in_tx_list)
                #print(devices_to_be_analized.getDeviceDistancesFromGateways(idx))
                
                #simulate if you have success in the communication, considering the transmission signal of the interferents
                rx_success_in_cycle = 0
                rx_success = 0
                for i in range(REPTION_TIMES_PER_INTERACTION_Q1_SIM):        
                    bool_rx_success = 0
                    for idx_gw, gateway in enumerate(devices_interferents.getGateways()):
                        done = 0
                        h_d1 = sqrt_0_5*abs(np.random.randn(1) + np.random.randn(1)*j )
                        main_device_distance_to_gateway = devices_to_be_analized.getDeviceDistancesFromGateways(idx)[idx_gw]
                        main_device_path_loss = friisEquation(main_device_distance_to_gateway, n)
                        main_device_power = dBm2mW(devices_to_be_analized.getTransmissionPower(idx))
                        main_device_rx_signal = (main_device_power*main_device_path_loss*h_d1**2)
                        
                        for idx_interferent in interfent_in_tx_list:
                            h_d1 = sqrt_0_5*abs(np.random.randn(1) + np.random.randn(1)*j )
                            interferent_distance_to_gateway = devices_interferents.getDeviceDistancesFromGateways(idx_interferent)[idx_gw]
                            interferent_path_loss = friisEquation(interferent_distance_to_gateway, n)
                            interferent_power = dBm2mW(devices_interferents.getTransmissionPower(idx_interferent))
                            interferent_rx_signal = (interferent_power*interferent_path_loss*h_d1**2)*4
                            if main_device_rx_signal > (interferent_rx_signal):
                                bool_rx_success = 1
                                done = 1
                                break
                        if done:
                            break
                    rx_success = rx_success + bool_rx_success
                rx_success_in_cycle = rx_success/REPTION_TIMES_PER_INTERACTION_Q1_SIM
                rx_success_total = rx_success_total + rx_success_in_cycle
            else:
                rx_success_total = rx_success_total + 1

            #define the devices in the interferent list that is transmiting in same time 
            devices_outages[idx] = devices_outages[idx] + rx_success_total
        del devices_interferents
        
    for idx in range(devices_to_be_analized.getNumberOfDevices() - 1):
        devices_outages[idx] = devices_outages[idx]/REPTION_TIMES_CYCLES
        devices_to_be_analized.setQ1Probability(idx, devices_outages[idx])
        print("SF - %d, outage - %f"%(devices_to_be_analized.getSFNumber(idx), devices_outages[idx]))
    return 

def Q1WithShiftedGateway(distance, number_of_devices, gateway_possition, max_distance):
    """
    gateway_possition = (x,y)
    """
    multiplication_factor = 1
    devices = DeviceDistribuition(number_of_devices*multiplication_factor)

    sf_virtual_point, int_sf = getSF(distance)

    
    devices.averageDevicesDistribuition(gateway_possition)
    
    #devices = [device for device in devices_list if device[3][0]  == sf_virtual_point ]
    #print(devices_list)
    device_same_sf = devices.getDeviceInEachSF()[int_sf - 7]
    print(sf_virtual_point + " distance: " + str(distance) + "devices same sf " + str(device_same_sf))


    return Q1OutageProbability(distance, device_same_sf, max_distance, sf=int_sf)

def H1Simulated(sf, distance, n=2.75, power_tx=19, bw = 125e3):

    """
    """
    pl_tx = (10**(power_tx/10))/1e3
    sensibility = (10**(loraSensitivity(sf, bw)/10))/1e3
    sum = 0

    for i in range(REPTION_TIMES):
        h_d1 = math.sqrt(0.5)*abs(np.random.randn(1) + np.random.randn(1)*j )
        sum = sum + ((pl_tx*friisEquation(distance, n)*h_d1**2) >= sensibility)

    return sum/REPTION_TIMES

def Q1Simulated(distance, number_of_devices = 500, max_distance = 12000):
    """
        number_of_devices: is the number of devices in the same circus and same SF, 500/6 = 83
    """
    devices = DeviceDistribuition(number_of_devices)
    rx_success_total = 0.0

    #set the number of devices in the same SF (radius)
    sf_virtual_point, int_sf = getSF(distance)
    devices.averageDevicesDistribuition()
    [l0, l1, circul] = radiusPerDistance(distance, max_distance)
    number_of_devices_same_sf = devices.getDeviceInEachSF()[circul-1]

    return Q1OutageProbability(distance, number_of_devices_same_sf, max_distance, sf=int_sf)

   
    

def Q1OutageProbability(distance, device_with_same_sf, max_distance, n=2.75, sf=7):

    rx_success_total = 0.0
    #optmization
    friss_equation_distance = friisEquation(distance, n)
    sqrt_0_5 = math.sqrt(0.5)
    for cycle in range(REPTION_TIMES_CYCLES):

        devices_in_tx = 0
        distance_of_devices = []
        rx_success = 0.0
        
        #get the number of devices that is transmitting in the same time
        devices_in_tx = getDevicesInTx(device_with_same_sf, sf =sf)
        if(devices_in_tx > 0):
            #Debug
            # print(devices_per_cicle)
            #print("number_of_devices_same_sf %d"% number_of_devices_same_sf)
            #print("devices in tx %d"% devices_in_tx)

            #set the distance of the interferent devices
            for i in range(devices_in_tx):
                [l0, l1, circul] = radiusPerDistance(distance, max_distance)
                distance_of_devices.append(randint(l0, l1))
                #print("Distance of device %d"%distance_of_devices[i])
            
            #simulate if you have success in the communication, considering the transmission signal of the interferents
            for i in range(REPTION_TIMES_PER_INTERACTION_Q1_SIM):

                h_d1 = sqrt_0_5*abs(np.random.randn(1) + np.random.randn(1)*j )
                main_device_rx_signal = (friss_equation_distance*h_d1**2)
                bool_rx_success = 1
                
                #Consider only the higher interferent
                interferent_device_rx_signal = 0
                for a in range(devices_in_tx):
                    interferent_h_d1 = sqrt_0_5*abs(np.random.randn(1) + np.random.randn(1)*j )
                    interferent_device_rx_signal = ((friisEquation(distance_of_devices[a], n)*interferent_h_d1**2))*4
                    #bool_rx_success = 0 if main_device_rx_signal < interferent_device_rx_signal else 1
                    if main_device_rx_signal < (interferent_device_rx_signal):
                        bool_rx_success = 0
                        break            
                #consider the sum of all interferents
                """interferent_device_rx_signal = 0
                for a in range(devices_in_tx):
                    interferent_h_d1 = math.sqrt(0.5)*abs(np.random.randn(1) + np.random.randn(1)*j )
                    interferent_device_rx_signal = interferent_device_rx_signal + ((friisEquation(distance_of_devices[a], n)*interferent_h_d1**2))
                if((main_device_rx_signal < interferent_device_rx_signal*4)):
                    bool_rx_success = 0
                    break
                """
                rx_success = rx_success + bool_rx_success
            rx_success_in_cycle = rx_success/REPTION_TIMES_PER_INTERACTION_Q1_SIM
            #print("cycle: %d - rx_success: %d - rx_success_in_cycle: %f"% (cycle, rx_success, rx_success_in_cycle))
            rx_success_total = rx_success_total + rx_success_in_cycle
        else:
            rx_success_total = rx_success_total + 1
    
    return (rx_success_total/REPTION_TIMES_CYCLES)

