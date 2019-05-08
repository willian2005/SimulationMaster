import math 
from random import randint

RADIUS = 12000 #don't change this parameter
x_central = 12000 #don't change this parameter
y_central = 12000 #don't change this parameter

def __deviceDistribuition(number_of_devices, bottom_radius, higher_radius):

    devices_list_possitions = []
    for i in range(number_of_devices):
        distance_from_center = 2*higher_radius 
        while(distance_from_center < bottom_radius or distance_from_center > higher_radius):
            x = randint(0, higher_radius + x_central)
            y = randint(0, higher_radius + y_central)
            distance_from_center = math.sqrt(abs(x - x_central)**2 + abs(y - y_central)**2)
        
        devices_list_possitions.append((x, y, distance_from_center))
    return devices_list_possitions    
        



def radiusPerDistance(distance):
    """
        Return the minimum radius and maximum radius to the same SF
    """    
    if distance < 2000:
        l0 = 1
        l1 = 2000   
        in_radius = 1 
    elif distance < 4000: 
        l0 = 2000
        l1 = 4000
        in_radius = 2
    elif distance < 6000:
        l0 = 4000
        l1 = 6000
        in_radius = 3
    elif distance < 8000:
        l0 = 6000
        l1 = 8000
        in_radius = 4
    elif distance < 10000:
        l0 = 8000
        l1 = 10000
        in_radius = 5
    else:
        l0 = 10000
        l1 = 12000
        in_radius = 6
    return l0, l1, in_radius

def averageDevicesDistribuition(number_of_devices):

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
        devices_list_possitions.extend(__deviceDistribuition(number_of_devices_per_circle, i+1, i+step))

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