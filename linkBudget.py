# -174 + 10*log10(125000) +(6) +(-15)
import math

def friisEquation(distance, n =2.75, fc = 868e6):
    """
    Parameters
        distance: the distance in meters
        n: propagation coefficient
        fc: frequency used the transmit the information
    Return:
        link budget need used to transmit the information
    """
    
    c = float(3e8)        # m/s^2 - c
    l = float(c/fc)      # meters - wavelength
    g = math.pow( float(l/((4*math.pi)*distance)), float(n))
    return g