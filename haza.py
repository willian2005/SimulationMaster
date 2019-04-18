import math 
from loraSpecific import *
from mathUtils import *
from linkBudget import friisEquation

def H1Theorical(sf, distance, power_tx=19):

    """
    #H1 Theory
    #equation (6) in the paper
    #H1t = exp(-((Noise*SNR(ring_d1))./(Ptx*g(d1))));
    """
    pl_tx = (10**(power_tx/10))/1e3
    hlt = math.exp(-(varianceWhiteNoise()*SNR_qsf_linear(sf))/(pl_tx*friisEquation(distance)))
    return hlt
