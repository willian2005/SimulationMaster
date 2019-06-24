import math 
from random import randint
import numpy as np
from loraSpecific import *
import matplotlib.pyplot as plt
import _pickle as cPickle
from time import gmtime, strftime


RADIUS = 12000
x_central = 12000 
y_central = 12000 
class DeviceDistribuition():

    def __init__(self, number_of_devices):
        self.number_of_devices = number_of_devices
        self.coordenate_list = [0]*number_of_devices
        self.sf_list = [0]*number_of_devices
        self.distance_from_gateway = [0]*number_of_devices
        self.q1_probability = [0]*number_of_devices
        self.gateway_list = []
        self.add_devices = 0
    
    def __del__(self):
        del self.number_of_devices
        del self.coordenate_list
        del self.sf_list
        del self.distance_from_gateway
        del self.gateway_list
        
    def __deviceDistribuition(self, devices_in_circle, bottom_radius, higher_radius):
    
        for i in range(devices_in_circle):
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
            
            self.coordenate_list[self.add_devices] = [x, y]
            self.add_devices = self.add_devices + 1

    def __setGatewayDistance(self):

        for idx in range(self.number_of_devices -1):
            distances = []
            for gateway_possition in self.gateway_list:
                distance = math.sqrt(abs(self.getX(idx) - gateway_possition[0])**2 + abs( self.getY(idx) - gateway_possition[1])**2)
                distances.append(distance)
            
            self.distance_from_gateway[idx] = distances
        
    #in this function the device_list should have the gateway possition
    def __setSf(self):

        for idx in range(self.number_of_devices -1):
            sf = getSF(min(self.getDeviceDistancesFromGateways(idx)))    

            self.sf_list[idx] = sf

    def setQ1probability(self, index, q1):
        self.q1_probability[index] = q1

    def getQ1probability(self, index):
        return self.q1_probability[index]

    def getSFName(self, index):
        return self.sf_list[index][0]

    def getSFNumber(self, index):
        return self.sf_list[index][1]
    
    def getDevicesSameSF(self, sf):

        same_sf_list = []
        for i in range(self.getNumberOfDevices() - 1):
            if self.getSFName(i)  == sf or self.getSFNumber(i) == sf:
                same_sf_list.append(i)

        return same_sf_list

    def getX(self, index):
        return self.coordenate_list[index][0]

    def getY(self, index):
        return self.coordenate_list[index][1]

    def getDeviceDistancesFromGateways(self, index):
        return self.distance_from_gateway[index]
    
    def getNumberOfDevices(self):
        return self.number_of_devices
        
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

    def saveObjectData(self, file_name):
        
        f = open("./output_data/"+"DeviceDistribuition_"+file_name+strftime("%Y-%m-%d_%H:%M", gmtime())+".plt", 'wb')
        cPickle.dump(self.__dict__, f, 2)
        f.close()
   
    def loadObjectData(self, file_name):
        
        f = open(file_name, 'rb')
        tmp_dict = cPickle.load(f)
        f.close()          

        self.__dict__.update(tmp_dict) 
 
    def plotQ1Devices(self, title):

        plt.figure()
        #cm = plt.cm.get_cmap('RdYlBu')
        cm = plt.cm.get_cmap('BuGn')
        x = []
        y = []
        value = []
        for i in range(self.getNumberOfDevices() - 1):
            x.append(self.getX(i))
            y.append(self.getY(i))
            value.append(self.getQ1probability(i))

        sc = plt.scatter(x, y, c=value, vmin=min(value), vmax=1, cmap=cm)
    
        plt.colorbar(sc)
        plt.show()

    def plotQ1Histogram(self, title, hist_type = 'step'):

        plt.close('all')
        plt.figure(1)
        sf7 = []
        sf8 = []
        sf9 = []
        sf10 = []
        sf11 = []
        sf12 = []
        
        for i in range(self.getNumberOfDevices() - 1):
            
            if self.getSFNumber(i) == 7:
                sf7.append(self.getQ1probability(i))
            elif self.getSFNumber(i) == 8:
                sf8.append(self.getQ1probability(i))
            elif self.getSFNumber(i) == 9:
                sf9.append(self.getQ1probability(i))
            elif self.getSFNumber(i) == 10:
                sf10.append(self.getQ1probability(i))
            elif self.getSFNumber(i) == 11:
                sf11.append(self.getQ1probability(i))
            elif self.getSFNumber(i) == 12:
                sf12.append(self.getQ1probability(i))


        plt.title(title)
        if(len(sf7) > 0):
            plt.hist(sf7, histtype=hist_type, color="blue", label="SF7")    
        if(len(sf8) > 0):
            plt.hist(sf8, histtype=hist_type, color="green", label="SF8") 
        if(len(sf9) > 0):
            plt.hist(sf9, histtype=hist_type, color="yellow", label="SF9") 
        if(len(sf10) > 0):
            plt.hist(sf10, histtype=hist_type, color="pink",  label="SF10") 
        if(len(sf11) > 0):
            plt.hist(sf11, histtype=hist_type, color="black", label="SF11") 
        if(len(sf12) > 0):
            plt.hist(sf12, histtype=hist_type, color="brown", label="SF12") 

        plt.legend(loc='upper right')
        plt.show()

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

    def averageDevicesDistribuition(self, gateway_possition = [(x_central, y_central)]):

        total_area = math.pi*(RADIUS**2)
        step = 400
        self.gateway_list = gateway_possition
        devices_per_circle = []
        for i in range(0, RADIUS, step):
            internal_circle = math.pi*(i**2)
            external_circle = math.pi*((i+step)**2)
            circular_area = external_circle - internal_circle
            number_of_devices_per_circle = round((circular_area/total_area)*self.number_of_devices)
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