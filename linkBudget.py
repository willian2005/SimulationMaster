# -174 + 10*log10(125000) +(6) +(-15)
import math

snr_per_sf = [(7, -7.5), (8, -10), (9, -12.5), (10, -15), (11, -17.5), (12, -20)]

def loraSensitivity(sf, bw):
    """
    Parameters
        sf: sf desired from 7 to 12
        bw: the bandwidth used, normally (125000, 250000, 500000)
    """
    NF = 6

    for sf_base, snr in snr_per_sf:
        if sf == sf_base:
            sensitivity = -174 + 10*math.log10(bw) + NF + snr
    
    return sensitivity