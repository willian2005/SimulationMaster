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
    
    c = 3e8        # m/s^2 - c
    l = c/fc      # meters - wavelength
    g = math.pow((l/((4*math.pi)*distance)), n)
    return g