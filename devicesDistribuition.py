import math 
from random import randint
from loraSpecific import *

RADIUS = 12000 #don't change this parameter
x_central = 12000 #don't change this parameter
y_central = 12000 #don't change this parameter

def __deviceDistribuition(number_of_devices, bottom_radius, higher_radius, gateway_possition = (x_central, y_central)):

    devices_list_possitions = []
    for i in range(number_of_devices):
        distance_from_center = 2*higher_radius 
        while(distance_from_center < bottom_radius or distance_from_center > higher_radius):
            x = randint(0, higher_radius + x_central)
            y = randint(0, higher_radius + y_central)
            distance_from_center = math.sqrt(abs(x - x_central)**2 + abs(y - y_central)**2)
        
        distance_from_gateway = math.sqrt(abs(x - gateway_possition[0])**2 + abs(y - gateway_possition[1])**2)
        sf = getSF(distance_from_gateway)
        devices_list_possitions.append((x, y, distance_from_gateway, sf))
    return devices_list_possitions      

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

def averageDevicesDistribuition(number_of_devices, gateway_possition = (x_central, y_central)):

    total_area = math.pi*(RADIUS**2)
    step = 1000
    devices_list_possitions = []
    devices_per_circle = []
    for i in range(0, RADIUS, step):
        internal_circle = math.pi*(i**2)
        external_circle = math.pi*((i+step)**2)
        circular_area = external_circle - internal_circle
        number_of_devices_per_circle = round((circular_area/total_area)*number_of_devices)
        devices_per_circle.append(number_of_devices_per_circle)
        devices_list_possitions.extend(__deviceDistribuition(number_of_devices_per_circle, i+1, i+step, gateway_possition))

    return devices_list_possitions, devices_per_circle

def randomDevicesDistribuition(number_of_devices):

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