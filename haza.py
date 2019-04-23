import math 
from mpmath import *

from loraSpecific import *
from mathUtils import *
from linkBudget import friisEquation

def H1Theorical(sf, distance,  n =2.75, power_tx=19):

    """
    #H1 Theory
    #equation (6) in the paper
    #H1t = exp(-((Noise*SNR(ring_d1))./(Ptx*g(d1))));
    """
    pl_tx = (10**(power_tx/10))/1e3
    hlt = math.exp(-(varianceWhiteNoise()*SNR_qsf_linear(sf))/(pl_tx*friisEquation(distance, n=n)))
    return hlt

def Q1Theorical(distance, number_of_devices = 500, n=2.75, power_tx=19):
    
    R = 12000
    V = math.pi*(R**2)
    rho = number_of_devices/V
    p0 = 1/100
    #exp(-2*pi*rho*p0*((((l1.^2)./2).*hypergeom([1,2/n], 1+(2/n), -((l1.^n)./((d1.^n)*SIR)))) - (((l0.^2)./2).*hypergeom([1,2/n], 1+(2/n), -((l0.^n)./((d1.^n)*SIR))))));
    SIR = 10**(6/10)
    if distance < 2000:
        l0 = 0
        l1 = 2000    
    elif distance < 4000: 
        l0 = 2000
        l1 = 4000
    elif distance < 6000:
        l0 = 4000
        l1 = 6000
    elif distance < 8000:
        l0 = 6000
        l1 = 8000
    elif distance < 10000:
        l0 = 8000
        l1 = 10000
    else:
        l0 = 10000
        l1 = 12000
    #((((l1**2)/2)*hyper([1,2/n], [1+(2/n)], -((l1**n)/((distance**n)*SIR)))) - (((l0**2)/2)*hyper([1,2/n], [1+(2/n)], -((l0**n)/((distance**n)*SIR)))))
    return math.exp(-2*math.pi*rho*p0*((((l1**2)/2)*hyper([1,2/n], [1+(2/n)], -((l1**n)/((distance**n)*SIR)))) - (((l0**2)/2)*hyper([1,2/n], [1+(2/n)], -((l0**n)/((distance**n)*SIR))))))