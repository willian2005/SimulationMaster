import math 
from random import randint
import numpy as np
from loraSpecific import *
import matplotlib.pyplot as plt

RADIUS = 12000
x_central = 12000 
y_central = 12000 
class DeviceDistribuition():

    def __init__(self):
        self.devices_list = []
        self.gateway_list = []
    
    def __del__(self):
        del self.devices_list
        del self.gateway_list
        
    def __deviceDistribuition(self, number_of_devices, bottom_radius, higher_radius):
    
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
            
            self.devices_list.append([[x, y]])

    def __setGatewayDistance(self):

        for idx, device in enumerate(self.devices_list):
            distances = []
            for gateway_possition in self.gateway_list:
                distance = math.sqrt(abs(self.getX(idx) - gateway_possition[0])**2 + abs( self.getY(idx) - gateway_possition[1])**2)
                distances.append(distance)
            device = device + [distances]
            self.devices_list[idx] = device
        
    #in this function the device_list should have the gateway possition
    def __setSf(self):

        for idx, device in enumerate(self.devices_list):
            sf = getSF(min(self.getDeviceDistancesFromGateways(idx)))    
            device = device + [sf]
            self.devices_list[idx] = device

    def getSFName(self, index):
        return self.devices_list[index][2][0]

    def getSFNumber(self, index):
        return self.devices_list[index][2][1]
    
    def getDevicesSameSF(self, sf):

        same_sf_list = []
        for i in range(self.getNumberOfDevices() - 1):
            if self.getSFName(i)  == sf or self.getSFNumber(i) == sf:
                same_sf_list.append(i)

        return same_sf_list

    def getX(self, index):
        return self.devices_list[index][0][0]

    def getY(self, index):
        return self.devices_list[index][0][1]

    def getDeviceDistancesFromGateways(self, index):
        return self.devices_list[index][1]
    
    def getNumberOfDevices(self):
        return len(self.devices_list) +1
    
    def getDevice(self, device_possition):
        return self.devices_list[device_possition]

    def getDeviceInEachSF(self):
        SF_list = ["SF7", "SF8", "SF9", "SF10", "SF11", "SF12"]
        SFs = []
        for i in range(len(SF_list)):
            sf = 0
            for j in range(self.getNumberOfDevices() - 1):
                if self.getSFName(j)  == SF_list[i] :
                    sf = sf +1
            SFs.append(sf)
        return SFs

    def plotDevices(self, title):

        plt.figure()

        for i in range(self.getNumberOfDevices() - 1):
            if self.getSFName(i) == "SF7":
                plt.scatter(self.getX(i), self.getY(i), c="blue", linewidths=0.01)
            elif self.getSFName(i) == "SF8": 
                plt.scatter(self.getX(i), self.getY(i), c="green", linewidths=0.01)
            elif self.getSFName(i) == "SF9":
                plt.scatter(self.getX(i), self.getY(i), c="yellow", linewidths=0.01)
            elif self.getSFName(i) == "SF10":
                plt.scatter(self.getX(i), self.getY(i), c="pink", linewidths=0.01)
            elif self.getSFName(i) == "SF11":
                plt.scatter(self.getX(i), self.getY(i), c="black", linewidths=0.01)
            elif self.getSFName(i) == "SF12":
                plt.scatter(self.getX(i), self.getY(i), c="brown", linewidths=0.01)

        for gateway in self.gateway_list:
            plt.scatter(gateway[0], gateway[1], c="red")

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

        plt.legend(loc='upper right')
        plt.title(title)
        plt.show()

    def averageDevicesDistribuition(self, number_of_devices, gateway_possition = [(x_central, y_central)]):

        total_area = math.pi*(RADIUS**2)
        step = 2000
        self.gateway_list = gateway_possition
        devices_per_circle = []
        for i in range(0, RADIUS, step):
            internal_circle = math.pi*(i**2)
            external_circle = math.pi*((i+step)**2)
            circular_area = external_circle - internal_circle
            number_of_devices_per_circle = round((circular_area/total_area)*number_of_devices)
            devices_per_circle.append(number_of_devices_per_circle)
            self.__deviceDistribuition(number_of_devices_per_circle, i+1, i+step)

        self.__setGatewayDistance()
        self.__setSf()
    """
    def randomDevicesDistribuition(self, number_of_devices, gateways):

        devices_list_possitions = []

        #each radius is for each device
        #devices_per_radius [0] = (0, 2000) - [1] = (2000, 4000) - [2] = (4000, 6000) ....
        devices_per_radius = [0, 0, 0, 0, 0, 0]
        devices_list_possitions = self.__deviceDistribuition(number_of_devices, 1, RADIUS)
        for i in range(number_of_devices):
            circul = math.ceil(devices_list_possitions[i][2]/2000)
            devices_per_radius[circul - 1] = devices_per_radius[circul - 1] +1

        #Debug
        #for i in range(len(devices_list_possitions)):
        #    print("x: %d - y: %d - distance from center: %d"% (devices_list_possitions[i][0], devices_list_possitions[i][1], devices_list_possitions[i][2]))
        #print(devicesPerRadius)
        return devices_list_possitions, devices_per_radius
    """