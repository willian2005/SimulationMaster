import math 
from random import randint
import numpy as np
from loraTheoricalSimulation import *
from loraSpecific import *
import matplotlib.pyplot as plt
import _pickle as cPickle
from time import gmtime, strftime
import mplcursors
from operator import itemgetter, attrgetter

#RADIUS = 12000
#x_central = 12000 
#y_central = 12000 
class DeviceDistribuition():

    def __init__(self, number_of_devices = 0, gateway_possition = None, radius = 0, sf_method = 0, transmission_power = 14, power_method = "STATIC", H1_target=0.9, h1_mult_gateway_diversity = False):
        
        self.n = 2.75
        self.power_method = power_method
        self.sf_method = sf_method
        self.number_of_devices = number_of_devices
        self.coordenate_list = [0]*number_of_devices
        self.sf_list = [0]*number_of_devices
        self.distance_from_gateway = [0]*number_of_devices
        self.q1_probability = [0]*number_of_devices
        self.h1_probability = [0]*number_of_devices
        self.c1_probability = [0]*number_of_devices
        self.max_transmission_power_dbm = transmission_power
        self.transmission_power_dbm = [transmission_power]*number_of_devices
        self.gateway_list = gateway_possition
        self.radius = radius
        self.add_devices = 0
        self.H1_target = H1_target
        self.h1_mult_gateway_diversity = h1_mult_gateway_diversity
        
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
            x_central = self.radius
            y_central = self.radius
            x = np.cos(rad)*hypotenuse + x_central
            y = np.sin(rad)*hypotenuse + y_central            
            
            self.coordenate_list[self.add_devices] = [x, y]
            self.add_devices = self.add_devices + 1

    def __setGatewayDistance(self):

        print(self.gateway_list)
        for idx in range(self.number_of_devices -1):
            distances = []
            for gateway_possition in self.gateway_list:
                distance = math.sqrt(abs(self.getX(idx) - gateway_possition[0])**2 + abs( self.getY(idx) - gateway_possition[1])**2)
                distances.append(distance)
            
            self.distance_from_gateway[idx] = distances
        
    #in this function the device_list should have the gateway possition
    def __setSf(self):

        distance_from_closer_gateway = []

        for idx in range(self.number_of_devices -1):
            if(min(self.getDeviceDistancesFromGateways(idx)) ) < 100:          
                self.coordenate_list[idx] = [self.coordenate_list[idx][0] + 200 , self.coordenate_list[idx][1] + 200]

        self.__setGatewayDistance()

        for idx in range(self.number_of_devices -1):

            distance_from_closer_gateway.append((idx, min(self.getDeviceDistancesFromGateways(idx)))) 
        #ordem the devices from the closer gateway    
        distance_from_closer_gateway = sorted(distance_from_closer_gateway, key=itemgetter(1))
        print(len(self.gateway_list))
        for idx in range(self.number_of_devices -1):
            priority_device = distance_from_closer_gateway[idx][0]
            #   sf = getSF(min(self.getDeviceDistancesFromGateways(priority_device)), self.radius, self.sf_method, self.number_of_devices, self.H1_target, self.getTransmissionPower(idx))
            
            if self.h1_mult_gateway_diversity == True:
                sf = getSF(self.getDeviceDistancesFromGateways(priority_device), self.radius, self.sf_method, self.number_of_devices, self.n, self.H1_target, self.getTransmissionPower(idx), self.h1_mult_gateway_diversity, number_of_gateways=len(self.gateway_list))
            else:
                sf = getSF(min(self.getDeviceDistancesFromGateways(priority_device)), self.radius, self.sf_method, self.number_of_devices, self.n, self.H1_target, self.getTransmissionPower(idx), number_of_gateways=len(self.gateway_list))    
            
            self.sf_list[priority_device] = sf
    
    def __setAllDevicesInSf(self, sf):
        
        sfs = ["SF7", "SF8", "SF9", "SF10", "SF11", "SF12"]

        for idx in range(self.number_of_devices -1):    
            self.sf_list[idx] = [sfs[sf-7], sf]
            
    def __setPowerDevice(self):

        
        if self.power_method == "FULL_RANGE" or self.power_method == "LORA_RANGE":
            
            H1_target = self.H1_target
            for idx in range(self.number_of_devices -1):

                if self.h1_mult_gateway_diversity == True:
                    power = P1TheoricalFromH1MultGatewayDiversity(H1_target, self.getSFNumber(idx), self.getDeviceDistancesFromGateways(idx), self.n)
                else:
                    power = P1TheoricalFromH1(H1_target, self.getSFNumber(idx), min(self.getDeviceDistancesFromGateways(idx)), self.n)
    

                if self.power_method == "LORA_RANGE":
                    power = math.ceil(power)
                    if power < 2:
                        power = 2
                    elif power > self.max_transmission_power_dbm:
                        power = self.max_transmission_power_dbm
                self.setTransmissionPower(idx, power)
        
        return 0
                
    def updateC1Probability(self):
        
        for idx in range(self.number_of_devices -1):
            self.c1_probability[idx] = self.q1_probability[idx]*self.h1_probability[idx]
    
    def averageC1DER(self):
        
        sum = 0
        for idx in range(self.number_of_devices -1):
            sum = sum + self.c1_probability[idx]

        return sum/(self.number_of_devices -1)    
    
    def __div0Handler(self, a, b):
            try: 
                return a/b 
            except ZeroDivisionError: 
                return 0


    def getAverageBySF(self, parameter):

        sumBySF = [0,0,0,0,0,0]

        for idx in range(self.number_of_devices -1):    
            sf_idx =  self.getSFNumber(idx) - 7
            sumBySF[sf_idx] = sumBySF[sf_idx] + parameter(idx)

        return [float(f"%.3f"%self.__div0Handler(a, b)) for a, b in zip(sumBySF, self.getDeviceInEachSF())]
    
    def getQ1AverageBySF(self):

        return self.getAverageBySF(self.getQ1Probability)

    def getH1AverageBySF(self):

        return self.getAverageBySF(self.getH1Probability)

    def getTransmissionPowerAverageBySF(self):

        return self.getAverageBySF(self.getTransmissionPower)

    def getC1Probability(self, index):
        return self.c1_probability[index]

    def setH1Probability(self, index, h1):
        self.h1_probability[index] = h1

    def getH1Probability(self, index):
        return self.h1_probability[index]

    def setTransmissionPower(self, index, pot_dbm):
        self.transmission_power_dbm[index] = pot_dbm

    def getTransmissionPower(self, index):
        return self.transmission_power_dbm[index]


    def setQ1Probability(self, index, q1):
        self.q1_probability[index] = q1

    def getQ1Probability(self, index):
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

    def getGateways(self):
        return self.gateway_list

    def saveObjectData(self, file_name):
        
        f = open("./output_data/"+"DeviceDistribuition_"+file_name+strftime("%Y-%m-%d_%H_%M", gmtime())+".plt", 'wb')
        cPickle.dump(self.__dict__, f, 2)
        f.close()
   
    def loadObjectData(self, file_name):
        
        f = open(file_name, 'rb')
        tmp_dict = cPickle.load(f)
        f.close()          

        self.__dict__.update(tmp_dict) 
 
    def __plotDevices(self, code, title, plot_range):

        fig = plt.figure()
        #cm = plt.cm.get_cmap('RdYlBu')
        cm = plt.cm.get_cmap('BuGn')
        x = []
        y = []
        value = []
        labels = []
        
        for i in range(self.getNumberOfDevices() - 1):
            x.append(self.getX(i))
            y.append(self.getY(i))
            
            if code == "Q1_PROB":
                value.append(self.getQ1Probability(i))
                labels.append(""+str(self.getQ1Probability(i))+"\n"+str(self.getSFName(i)))
            elif code == "H1_PROB":
                value.append(self.getH1Probability(i))
                labels.append(""+str(self.getH1Probability(i))+"\n"+str(self.getSFName(i)))
            elif code == "C1_PROB":
                value.append(self.getC1Probability(i))
                labels.append(""+str(self.getC1Probability(i))+"\n"+str(self.getSFName(i)))
            elif code == "POWER":
                value.append(self.getTransmissionPower(i))
                labels.append(""+str(self.getTransmissionPower(i))+"\n"+str(self.getSFName(i)))
        
        if(plot_range == "1_min"):
            plt.scatter(x, y, c=value, vmin=min(value), vmax=1, cmap=cm)
            mplcursors.cursor(hover=True).connect(
                "add", lambda sel: sel.annotation.set_text(labels[sel.target.index]))
        elif(plot_range == "max_min"):
            plt.scatter(x, y, c=value, vmin=min(value), vmax=max(value), cmap=cm)        
            mplcursors.cursor(hover=True).connect(
                "add", lambda sel: sel.annotation.set_text(labels[sel.target.index]))
        


        plt.colorbar()
        for gateway in self.gateway_list:
           plt.scatter(gateway[0], gateway[1], color="red")
        plt.title(title, fontsize=18)
        plt.xlabel("Metros", fontsize=14)
        plt.ylabel("Metros", fontsize=14)
        #plt.grid(True)
        plt.savefig(str(title+code+".eps"), format='eps')
        plt.show()
        

    def plotQ1Devices(self, title, plot_range):
        self.__plotDevices("Q1_PROB", title, plot_range)
        
    def plotH1Devices(self, title, plot_range):
        self.__plotDevices("H1_PROB", title, plot_range)

    def plotC1Devices(self, title, plot_range):
        self.__plotDevices("C1_PROB", title, plot_range)

    def plotDevicesPower(self, title, plot_range):
        self.__plotDevices("POWER", title, plot_range)

    def plotHistogram(self, title, source, hist_type = 'step'):

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
                if source == "C1":
                    sf7.append(self.getC1Probability(i))
                elif source == "POWER":
                    sf7.append(self.getTransmissionPower(i))

            elif self.getSFNumber(i) == 8:
                if source == "C1":
                    sf8.append(self.getC1Probability(i))
                elif source == "POWER":
                    sf8.append(self.getTransmissionPower(i))

            elif self.getSFNumber(i) == 9:
                if source == "C1":
                    sf9.append(self.getC1Probability(i))
                elif source == "POWER":
                    sf9.append(self.getTransmissionPower(i))

            elif self.getSFNumber(i) == 10:
                if source == "C1":
                    sf10.append(self.getC1Probability(i))
                elif source == "POWER":
                    sf10.append(self.getTransmissionPower(i))

            elif self.getSFNumber(i) == 11:
                if source == "C1":
                    sf11.append(self.getC1Probability(i))
                elif source == "POWER":
                    sf11.append(self.getTransmissionPower(i))

            elif self.getSFNumber(i) == 12:
                if source == "C1":
                    sf12.append(self.getC1Probability(i))
                elif source == "POWER":
                    sf12.append(self.getTransmissionPower(i))

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
        
        plt.title(title, fontsize=18)
        plt.legend(loc='upper right')
        #plt.grid(True)
        if source == "C1":
            plt.savefig(str(title+"C1_histogram.eps"), format='eps')
        elif source == "POWER":
            plt.savefig(str(title+"POWER_histogram.eps"), format='eps')
        
        plt.show()

    def plotDevices(self, title):

        name_label = [0, 0, 0, 0, 0, 0, 0]
        plt.figure(figsize=(8, 8))

        for i in range(self.getNumberOfDevices() - 1):
            if self.getSFName(i) == "SF7":
                if name_label[0] == 0:
                    name_label[0] = 1
                    plt.scatter(self.getX(i), self.getY(i), c="blue", label='SF7', linewidths=0.01)
                else:
                    plt.scatter(self.getX(i), self.getY(i), c="blue", linewidths=0.01)
            elif self.getSFName(i) == "SF8": 
                if name_label[1] == 0:
                    name_label[1] = 1
                    plt.scatter(self.getX(i), self.getY(i), c="green", label='SF8', linewidths=0.01)
                else:
                    plt.scatter(self.getX(i), self.getY(i), c="green", linewidths=0.01)
            elif self.getSFName(i) == "SF9":
                if name_label[2] == 0:
                    name_label[2] = 1
                    plt.scatter(self.getX(i), self.getY(i), c="yellow", label='SF9', linewidths=0.01)
                else:
                    plt.scatter(self.getX(i), self.getY(i), c="yellow", linewidths=0.01)
            elif self.getSFName(i) == "SF10":
                if name_label[3] == 0:
                    name_label[3] = 1
                    plt.scatter(self.getX(i), self.getY(i), c="pink", label='SF10', linewidths=0.01)
                else:
                    plt.scatter(self.getX(i), self.getY(i), c="pink", linewidths=0.01)
            elif self.getSFName(i) == "SF11":
                if name_label[4] == 0:
                    name_label[4] = 1
                    plt.scatter(self.getX(i), self.getY(i), c="black", label='SF11', linewidths=0.01)
                else:
                    plt.scatter(self.getX(i), self.getY(i), c="black", linewidths=0.01)
            elif self.getSFName(i) == "SF12":
                if name_label[5] == 0:
                    name_label[5] = 1
                    plt.scatter(self.getX(i), self.getY(i), c="brown", label='SF12', linewidths=0.01)
                else:
                    plt.scatter(self.getX(i), self.getY(i), c="brown", linewidths=0.01)

        for gateway in self.gateway_list:
            if name_label[6] == 0:
                name_label[6] = 1
                plt.scatter(gateway[0], gateway[1], label="Gateway", c="red")
            else:
                plt.scatter(gateway[0], gateway[1], c="red")

        # plt.ylim(0, self.radius*2)
        # plt.xlim(0, self.radius*2)
        #need because of the legend
        # plt.scatter(1000, 1000, c="red", linewidths=0.01, label='Gateway')
        # plt.scatter(1000, 1000, c="blue", linewidths=0.01, label='SF7')
        # plt.scatter(1000, 1000, c="green", linewidths=0.01, label='SF8')
        # plt.scatter(1000, 1000, c="yellow", linewidths=0.01, label='SF9')
        # plt.scatter(1000, 1000, c="pink", linewidths=0.01, label='SF10')
        # plt.scatter(1000, 1000, c="black", linewidths=0.01, label='SF11')
        # plt.scatter(1000, 1000, c="brown", linewidths=0.01, label='SF12')

        plt.xlabel("Metros", fontsize=18)
        plt.ylabel("Metros", fontsize=18)
        plt.legend(loc='upper right', fontsize=12)
        #plt.title(title, fontsize=18)
        plt.axis('equal')

        plt.savefig(str("Device_distribuition.eps"), format='eps')
        
        plt.show()

    def averageDevicesDistribuition(self):

        number_of_steps = 30
        total_area = math.pi*((self.radius)**2)
        step = int((self.radius)/number_of_steps)
        devices_per_circle = []
        for i in range(0, int(self.radius), step):
            internal_circle = math.pi*(i**2)
            external_circle = math.pi*((i+step)**2)
            circular_area = external_circle - internal_circle
            number_of_devices_per_circle = math.ceil((circular_area/total_area)*(self.number_of_devices - 1))
            if(number_of_devices_per_circle + self.add_devices >= self.number_of_devices):
                number_of_devices_per_circle = (self.number_of_devices - self.add_devices) - 1
            devices_per_circle.append(number_of_devices_per_circle)
            self.__deviceDistribuition(number_of_devices_per_circle, i+1, i+step)
            print("internal circle: %d, external: %d"%(i+1, step))

        self.__setGatewayDistance()
        self.__setSf()
        self.__setPowerDevice()


    def specificySFDevicesDistribuition(self, sf):

        number_of_steps = 30
        total_area = math.pi*((self.radius)**2)
        step = int((self.radius)/number_of_steps)
        devices_per_circle = []
        for i in range(0, int(self.radius), step):
            internal_circle = math.pi*(i**2)
            external_circle = math.pi*((i+step)**2)
            circular_area = external_circle - internal_circle
            number_of_devices_per_circle = math.ceil((circular_area/total_area)*(self.number_of_devices - 1))
            if(number_of_devices_per_circle + self.add_devices >= self.number_of_devices):
                number_of_devices_per_circle = (self.number_of_devices - self.add_devices) - 1
            devices_per_circle.append(number_of_devices_per_circle)
            self.__deviceDistribuition(number_of_devices_per_circle, i+1, i+step)
            print("internal circle: %d, external: %d"%(i+1, step))

        self.__setGatewayDistance()
        self.__setAllDevicesInSf(sf)
        self.__setPowerDevice()






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