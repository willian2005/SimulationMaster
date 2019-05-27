import math 
from mpmath import *
import numpy as np
from random import randint

from loraSpecific import *
from mathUtils import *
from linkBudget import friisEquation
from devicesDistribuition import *

# Reproduction of "Low Power Wide Area Network Analysis: Can LoRa Scale?", 
# by Orestis Georgiou and Usman Raza - IEEE Wireless Communications Letter,
# Vol. 6, No. 2, Abril 2017.


REPTION_TIMES = 10000
REPTION_TIMES_PER_INTERACTION_Q1_SIM = 200
REPTION_TIMES_CYCLES = 500

DEVICES_TOTAL = 500

DEVICES_WITH_SAME_BAUDRATE      = 1     #All the SFs will transmit with the baudrate of the SF12
DEVICES_WITH_SAME_TIME_ON_AIR   = 2     #All the devices will transmit respecting the 1% rule (or less), SF7 will have higher baudrate 

TOA_METHOD = DEVICES_WITH_SAME_BAUDRATE
def getDevicesInTx(number_of_devices, method=DEVICES_WITH_SAME_BAUDRATE, sf=7):

    devices_in_tx = 0
    if(method == DEVICES_WITH_SAME_TIME_ON_AIR):
        time_using_channel = randint(1, 100) #using a channel in 1% of the time
        for i in range(number_of_devices):
            if randint(1, 100) == time_using_channel:
                devices_in_tx = devices_in_tx + 1
    
    elif(method == DEVICES_WITH_SAME_BAUDRATE):
    
        time_on_air_in_reference_sf12_list = [24.033195, 13.104072, 7.203980, 3.601990, 1.800995, 1.000000]
        time_on_air_in_reference_sf12 = round(time_on_air_in_reference_sf12_list[sf-7]*100)
        time_using_channel = randint(1, time_on_air_in_reference_sf12)#using a channel in 1% of the time
        #print("time_on_air_in_reference_sf12: %d, time_using_channel: %d"%(time_on_air_in_reference_sf12, time_using_channel))
        for i in range(number_of_devices):

            if randint(1, time_on_air_in_reference_sf12) == time_using_channel:
                devices_in_tx = devices_in_tx + 1
    
    return devices_in_tx

def H1Theorical(sf, distance,  n =2.75, power_tx=19):

    """
    #H1 Theory
    #equation (6) in the paper
    #H1t = exp(-((Noise*SNR(ring_d1))./(Ptx*g(d1))));
    """
    pl_tx = (10**(power_tx/10))/1e3
    hlt = math.exp(-(varianceWhiteNoise()*SNR_qsf_linear(sf))/(pl_tx*friisEquation(distance, n=n)))
    return hlt

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



def Q1WithShiftedGateway(distance, number_of_devices, gateway_possition, max_distance):
    """
    gateway_possition = (x,y)
    """

    multiplication_factor = 100
    sf_virtual_point, int_sf = getSF(distance)
    devices_list, devices_per_circle  = averageDevicesDistribuition(number_of_devices*multiplication_factor, gateway_possition)
    
    devices = [device for device in devices_list if device[3][0]  == sf_virtual_point ]
    #print(devices_list)
    device_same_sf = round(len(devices)/multiplication_factor)
    print(sf_virtual_point + " distance: " + str(distance) + "devices same sf " + str(device_same_sf))


    return Q1OutageProbability(distance, device_same_sf, max_distance, sf=int_sf)


def Q1Simulated(distance, number_of_devices = 500, max_distance = 12000):
    """
        number_of_devices: is the number of devices in the same circus and same SF, 500/6 = 83
    """
    rx_success_total = 0.0

    #set the number of devices in the same SF (radius)
    sf_virtual_point, int_sf = getSF(distance)
    device_list, devices_per_cicle = averageDevicesDistribuition(number_of_devices)
    [l0, l1, circul] = radiusPerDistance(distance, max_distance)
    number_of_devices_same_sf = devices_per_cicle[circul-1]

    return Q1OutageProbability(distance, number_of_devices_same_sf, max_distance, sf=int_sf)
    
def Q1Theorical(distance, number_of_devices = 500, n=2.75, power_tx=19, max_distance = 12000):
    
    R = 12000
    V = math.pi*(R**2)
    rho = number_of_devices/V
    p0 = 1/100
    SIR = 10**(6/10)

    [l0,l1, in_radius] = radiusPerDistance(distance, max_distance)

    return math.exp(-2*math.pi*rho*p0*((((l1**2)/2)*hyper([1,2/n], [1+(2/n)], -((l1**n)/((distance**n)*SIR)))) - (((l0**2)/2)*hyper([1,2/n], [1+(2/n)], -((l0**n)/((distance**n)*SIR))))))


