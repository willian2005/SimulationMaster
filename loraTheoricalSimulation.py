import math 
from mpmath import *
import numpy as np
from random import randint

from loraSpecific import *
from mathUtils import *
from linkBudget import friisEquation


# Reproduction of "Low Power Wide Area Network Analysis: Can LoRa Scale?", 
# by Orestis Georgiou and Usman Raza - IEEE Wireless Communications Letter,
# Vol. 6, No. 2, Abril 2017.



def H1Theorical(sf, distance,  n =2.75, power_tx=19):

    """
    #H1 Theory
    #equation (6) in the paper
    #H1t = exp(-((Noise*SNR(ring_d1))./(Ptx*g(d1))));
    """
    pl_tx = (10**(power_tx/10))/1e3
    hlt = math.exp(-(varianceWhiteNoise()*SNR_qsf_linear(sf))/(pl_tx*friisEquation(distance, n=n)))
    return hlt


def P1TheoricalFromH1(H1, sf, distance, n=2.75):
    """
    Teste
    """
    P1_linear = -(varianceWhiteNoise()*SNR_qsf_linear(sf))/(friisEquation(distance, n=n)*math.log(H1)) 
    P1_dbm = mW2dBm(P1_linear*1000)
    return P1_dbm

    
def Q1Theorical(distance, number_of_devices = 500, n=2.75, power_tx=19, max_distance = 12000):
    
    R = 12000
    V = math.pi*(R**2)
    rho = number_of_devices/V
    p0 = 1/100
    SIR = 10**(6/10)

    [l0,l1, in_radius] = radiusPerDistance(distance, max_distance)

    return math.exp(-2*math.pi*rho*p0*((((l1**2)/2)*hyper([1,2/n], [1+(2/n)], -((l1**n)/((distance**n)*SIR)))) - (((l0**2)/2)*hyper([1,2/n], [1+(2/n)], -((l0**n)/((distance**n)*SIR))))))


