import math 
from random import randint
import numpy as np
from loraSpecific import *

RADIUS = 12000
x_central = 12000 
y_central = 12000 

def __deviceDistribuition(number_of_devices, bottom_radius, higher_radius):
 
    devices_list_possitions = []
    for i in range(number_of_devices):
        """
        distance_from_center = 2*higher_radius 
        while(distance_from_center < bottom_radius or distance_from_center > higher_radius):
            x = randint(0, higher_radius + x_central)
            y = randint(0, higher_radius + y_central)
            distance_from_center = math.sqrt(abs(x - x_central)**2 + abs(y - y_central)**2)
        
        distance_from_gateway = math.sqrt(abs(x - gateway_possition[0])**2 + abs(y - gateway_possition[1])**2)
        """
        
        hypotenuse = randint(bottom_radius, higher_radius)
        degree = randint(0, 360)
        rad = np.radians(degree)
        x = np.cos(rad)*hypotenuse + x_central
        y = np.sin(rad)*hypotenuse + y_central
        
        devices_list_possitions.append([[x, y]])
    return devices_list_possitions      

def __setGatewayDistance(device_list, gateway_list):

    for idx, device in enumerate(device_list):
        distances = []
        for gateway_possition in gateway_list:
            distance = math.sqrt(abs(getDeviceX(device) - gateway_possition[0])**2 + abs( getDeviceY(device) - gateway_possition[1])**2)
            distances.append(distance)
        device = device + [distances]
        device_list[idx] = device
    return device_list

#in this function the device_list should have the gateway possition
def __setSf(device_list):

    for idx, device in enumerate(device_list):
        sf = getSF(min(getDeviceDistancesFromGateways(device)))    
        device = device + [sf]
        device_list[idx] = device
    return device_list

def getDeviceSFName(device):
    return device[2][0]

def getDeviceSFNumber(device):
    return device[2][1]
    
def getDeviceX(device):
    return device[0][0]

def getDeviceY(device):
    return device[0][1]

def getDeviceDistancesFromGateways(device):
    return device[1]

def radiusPerDistance(distance, max_distance):
    """
        Return the minimum radius and maximum radius to the same SF
    """    
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

def averageDevicesDistribuition(number_of_devices, gateway_possition = [(x_central, y_central)]):

    total_area = math.pi*(RADIUS**2)
    step = 2000
    devices_list_possitions = []
    devices_per_circle = []
    for i in range(0, RADIUS, step):
        internal_circle = math.pi*(i**2)
        external_circle = math.pi*((i+step)**2)
        circular_area = external_circle - internal_circle
        number_of_devices_per_circle = round((circular_area/total_area)*number_of_devices)
        devices_per_circle.append(number_of_devices_per_circle)
        circle_device_distribuition = __deviceDistribuition(number_of_devices_per_circle, i+1, i+step)
        circle_device_distribuition = __setGatewayDistance(circle_device_distribuition, gateway_possition)
        circle_device_distribuition = __setSf(circle_device_distribuition)
        devices_list_possitions.extend(circle_device_distribuition)

    return devices_list_possitions, devices_per_circle

def randomDevicesDistribuition(number_of_devices, gateways):

    devices_list_possitions = []

    #each radius is for each device
    #devices_per_radius [0] = (0, 2000) - [1] = (2000, 4000) - [2] = (4000, 6000) ....
    devices_per_radius = [0, 0, 0, 0, 0, 0]
    devices_list_possitions = __deviceDistribuition(number_of_devices, 1, RADIUS)
    for i in range(number_of_devices):
        circul = math.ceil(devices_list_possitions[i][2]/2000)
        devices_per_radius[circul - 1] = devices_per_radius[circul - 1] +1

    #Debug
    #for i in range(len(devices_list_possitions)):
    #    print("x: %d - y: %d - distance from center: %d"% (devices_list_possitions[i][0], devices_list_possitions[i][1], devices_list_possitions[i][2]))
    #print(devicesPerRadius)
    return devices_list_possitions, devices_per_radius